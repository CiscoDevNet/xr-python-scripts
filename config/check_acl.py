"""
Config script to ensure an ACL of the given name exists on the provided interface when ACL related configuration is committed
"""

import cisco.config_validation as xr

from cisco.script_mgmt import xrlog
syslog = xrlog.getSysLogger('check_acl')

#These values should be changed as necessary
interface_name = "TenGigE0/0/0/10"
acl_name = "access-list-1"

def check_acl(root):
        #Get the interface with the given name
        int_config = root.get_node("/ifmgr-cfg:interface-configurations/interface-configuration[active='act',interface-name='%s']" %interface_name)
        if int_config:
                syslog.info("Interface found")

                #Retrieve the list of ACLs under the interface
                acl = int_config.get_list("/ip-pfilter-cfg:ipv4-packet-filter/inbound/acl-name-array")
                if acl:
                        syslog.info("ACL list found")

                        #Search for the ACL in the list
                        if acl_name in [x.value for x in acl]:
                                syslog.info("ACL found")
                        else:
                                syslog.error("ACL not found")

#Run script when ACL related config is pushed
xr.register_validate_callback(["/ifmgr-cfg:interface-configurations/ifmgr-cfg:interface-configuration/ip-pfilter-cfg:ipv4-packet-filter/*"], check_acl)