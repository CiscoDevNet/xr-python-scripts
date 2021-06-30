# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.

"""
This is a template for exec scripts

"""
#To connect to netconf client
from iosxr.netconf.netconf_lib import NetconfClient

#To generate syslogs
syslog = xrlog.getSysLogger('template_exec')

def test_exec():
    """
    Testcase for exec script
    """
    nc = NetconfClient(debug=True)
    nc.connect()
    #Netconf or processing operations
    nc.close()
    

if __name__ == '__main__':
    test_exec()
