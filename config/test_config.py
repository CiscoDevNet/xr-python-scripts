import cisco.config_validation as xr
import ipaddress

from cisco.script_mgmt import xrlog
logger = xrlog.getScriptLogger('xr_cli_config')
syslog = xrlog.getSysLogger('xr_cli_config')

def check_loopback(root):
    int_config = root.get_node("/ifmgr-cfg:interface-configurations/interface-configuration[active='act',interface-name='Loopback21041989']")
    if int_config:
        ip_address = int_config.get_node("ipv4-io-cfg:ipv4-network/addresses/primary/address")
        syslog.info("ipaddress is " + ip_address.value)
        syslog.info(str(ipaddress.ip_address(ip_address.value) not in ipaddress.ip_network("100.0.0.0/8")))
        if ipaddress.ip_address(ip_address.value) not in ipaddress.ip_network("100.0.0.0/8"): 
            xr.add_error(ip_address,"Invalid ip address, please add in range 100.0.0.0")  
        netmask = int_config.get_node("ipv4-io-cfg:ipv4-network/addresses/primary/netmask")
        syslog.info(netmask.value)
        if netmask.value != "255.255.255.255":
            netmask.set_node(None,"255.255.255.255")
xr.register_validate_callback(["/ifmgr-cfg:interface-configurations/interface-configuration/*"],check_loopback)

