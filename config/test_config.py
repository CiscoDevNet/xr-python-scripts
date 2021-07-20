# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.
"""
Validate user configuration on loopback interface.

It checks for IP address to be in a certain range else shows an error and checks for netmask, if netmask does not match the validation the script changes it.

Configuration to enable this feature:
configuration validation scripts

Please follow README.MD to add and configure this script. 

The loopback used in this script is Loopback 21041989 but you can change it by modifying the global variable loopback.

To test script try configuration other than 100.0.0.0 network and mask other than 32:

RP/0/RP0/CPU0:ios(config)#int loopback 21041989
RP/0/RP0/CPU0:ios(config-if)#ipv4 address 10.10.10.10/24
RP/0/RP0/CPU0:ios(config-if)#commit
Tue Jun 22 16:55:27.392 UTC

% Failed to commit one or more configuration items during an atomic operation. No changes have been made. Please issue 'show configuration failed if-committed' from this session to view the errors
RP/0/RP0/CPU0:ios(config-if)#show configuration failed 
Tue Jun 22 16:55:33.104 UTC
!! SEMANTIC ERRORS: This configuration was rejected by 
!! the system due to semantic errors. The individual 
!! errors with each failed configuration command can be 
!! found below.


interface Loopback21041989
 ipv4 address 10.10.10.10 255.255.255.0
!!% ERROR: Invalid ip address, please add in range 100.0.0.0/8
!
end

RP/0/RP0/CPU0:ios(config)#int loopback 21041989           
RP/0/RP0/CPU0:ios(config-if)#ipv4 address 100.100.100.100/24 
RP/0/RP0/CPU0:ios(config-if)#validate config-scripts apply-policy-modifications 
Tue Jun 22 16:57:24.061 UTC

% Policy modifications were made to target configuration, please issue 'show configuration' from this session to view the resulting configuration
RP/0/RP0/CPU0:ios(config-if)#show configuration 
Tue Jun 22 16:57:26.804 UTC
Building configuration...
!! IOS XR Configuration 7.5.1.09I
interface Loopback21041989
 ipv4 address 100.100.100.100 255.255.255.255
!
end

"""

import cisco.config_validation as xr
import ipaddress

from cisco.script_mgmt import xrlog
syslog = xrlog.getSysLogger('xr_cli_config')

loopback = 'Loopback21041989'
network = "100.0.0.0/8"
mask = "255.255.255.255"

def check_loopback(root):
    int_config = root.get_node("/ifmgr-cfg:interface-configurations/interface-configuration[active='act',interface-name=%s]" %loopback)
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
            
            
xr.register_validate_callback(["/ifmgr-cfg:interface-configurations/interface-configuration/ipv4-io-cfg:ipv4-network/addresses/primary/*"],check_loopback)

