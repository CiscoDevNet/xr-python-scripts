# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.
"""
Template for process scripts

Any exec script can be used as a process script

To trigger script
Step 1: Add and configure script as shown in README.MD

Step 2: Register the application with Appmgr

Configuraton:
appmgr process-script my-process-app
executable test_process.py
run args --threshold <threshold-value>

Step 3: Activate the registered application
appmgr process-script activate name my-process-app

Step 4: Check script status
show appmgr process-script-table

RP/0/RP0/CPU0:ios#show appmgr process-script-table
Thu Jan 21 18:15:03.201 UTC
Name             Executable         Activated    Status     Restart Policy   Config Pending
---------------  ------------------ --------- ------------- ---------------- --------------
my-process-app   test_process.py      Yes       Running    On Failure            No

Step 5: More operations
RP/0/RP0/CPU0:ios#appmgr process-script ?
  activate    Activate process script
  deactivate  Deactivate process script
  kill        Kill process script
  restart     Restart process script
  start       Start process script
  stop        Stop process script
""" 

#To connect to netconf client
from iosxr.netconf.netconf_lib import NetconfClient

#To generate syslogs
syslog = xrlog.getSysLogger('template_exec')

def test_process():
    """
    Testcase for process script
    """
    nc = NetconfClient(debug=True)
    nc.connect()
    #Netconf or any other operations
    nc.close()
    

if __name__ == '__main__':
    test_process()
