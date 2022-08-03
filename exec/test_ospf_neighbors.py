"""
How to run:
Use proper aaa settings:
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

script add exec /harddisk: test_ospf_neighbors.py
conf

script exec test_ospf_neighbors.py checksum sha256sum <sum>
commit
end

script run test_ospf_neighbors.py arguments <router-id> <interface> '--process' <process #> '--area' <area #>

Example:
script run test_ospf_neighbors.py arguments '10.1.1.4' 'HundredGigE0/0/0/32'
or
script run test_ospf_neighbors.py arguments '10.1.1.4' 'HundredGigE0/0/0/32' '--process' 100 '--area' 0

How to verify:
show logging last 10
check for 'SCRIPT : Configuration succeeded'
"""
import argparse
from iosxr.xrcli.xrcli_helper import *
from cisco.script_mgmt import xrlog

syslog = xrlog.getSysLogger('OSPF neighbor configuration')
helper = XrcliHelper(debug = True)

def ospf_neighbors():
	parser = argparse.ArgumentParser()

	#optional and positional arguments
	parser.add_argument("routerid", help = "ip address of router", type = str)
	parser.add_argument("interface", help = "interface for OSPF configuration", type = str)
	parser.add_argument("--process", help = "process for OSPF configuration", type = int, default = 100)
	parser.add_argument("--area", help = "area for OSPF configuration", type = int, default = 0)
	args = parser.parse_args()
	router_id = args.routerid
	interface_name = args.interface
	process_id = args.process
	area_id = args.area

	#This is identical to issuing the following commands in the configuration terminal
	#(config) router ospf <process_number>
	#(config-ospf) router-id <routerid>
	#(config-ospf) area <area> interface <interface>
	#(config-ospf-ar-if) network point-to-point
	#(config-ospf-ar-if) commit

	result = helper.xr_apply_config_string("router ospf %s \n\r router-id %s \n\r area %s interface %s \n\r network point-to-point" %(process_id, router_id, area_id, interface_name))
	
	#print status messages to syslogx
	if result['status'] == 'success':
        syslog.info('SCRIPT : Configuration succeeded')
    else:
        syslog.error('SCRIPT : Configuration failed')

if __name__ == '__main__':
	ospf_neighbors()