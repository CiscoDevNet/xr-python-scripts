"""
This script validates the user configuration on a loopback interface.
It checks for IP address to be in a certain range else shows an error and checks for netmask, if netmask does not match the validation the script changes it.

Configuration to enable this feature:
configuration validation scripts
"""

import cisco.config_validation as xr
import ipaddress

from cisco.script_mgmt import xrlog
syslog = xrlog.getSysLogger('xr_cli_config')

loopback = 'Loopback21041989'
network = "100.0.0.0/8"
mask = "255.255.255.255"

def check_loopback(root):
    int_config = root.get_node("/ifmgr-cfg:interface-configurations/interface-configuration[active='act',interface-name='%s']" %loopback)
    if int_config:
        ip_address = int_config.get_node("ipv4-io-cfg:ipv4-network/addresses/primary/address")
        syslog.info("ipaddress is " + ip_address.value)
        syslog.info(str(ipaddress.ip_address(ip_address.value) not in ipaddress.ip_network(network)))
        if ipaddress.ip_address(ip_address.value) not in ipaddress.ip_network(network): 
            xr.add_error(ip_address,"Invalid ip address, please add in range "+ network)  
        netmask = int_config.get_node("ipv4-io-cfg:ipv4-network/addresses/primary/netmask")
        syslog.info(netmask.value)
        if netmask.value != mask:
            netmask.set_node(None,mask)
            
            
xr.register_validate_callback(["/ifmgr-cfg:interface-configurations/interface-configuration/*"],check_loopback)

