"""
Config script to set a BGP router id when any BGP configuration is committed.
"""
import cisco.config_validation as xr
from cisco.script_mgmt import xrlog

syslog = xrlog.getSysLogger('check_bgp')

#These should be edited to match desired values
instance_name = "default"
instance_as = 0
four_byte_as = 100
router_id = "10.1.1.1"

def check_bgp(root):

	#Gets the autonomous system related to the BGP instance
	aut_sys = root.get_node("/ipv4-bgp-cfg:bgp/instance[instance-name='%s']/instance-as[as=%i]/four-byte-as[as=%i]/default-vrf" %(instance_name, instance_as, four_byte_as))
	if aut_sys:
		syslog.info("AS found")
		
		#Set the global BGP router id
		aut_sys.set_node("/global/router-id", router_id)
		syslog.info("New router id: %s" %aut_sys.get_node("/global/router-id").value)
	else:
		syslog.info("AS not found")	
			
#Run this script when any BGP related commit is pushed
xr.register_validate_callback(["/ipv4-bgp-cfg:bgp/instance/instance-as/*"], check_bgp)
