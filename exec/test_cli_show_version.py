"""
This script executes show version on the routerr

Pre-requisite configuration on router:
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

How to run?
script run exec <path> test_cli_show_version.py
eg: script run /harddisk\: test_cli_show_version.py

Configuration: 
None

Verify:
show logging last 10 
check for syslog: 'SCRIPT : Show version successful'
""" 
from iosxr.xrcli.xrcli_helper import XrcliHelper
from cisco.script_mgmt import xrlog

logger = xrlog.getScriptLogger('test_cli_show_version.py')
syslog = xrlog.getSysLogger('test_cli_show_version.py')
helper = XrcliHelper(debug = True)

if __name__ == '__main__':
        cmd = "show version"
        result = helper.xrcli_exec(cmd)
        print(result)
        if result['status'] == 'success':
            syslog.info('SCRIPT : Show version successful')
        else:
            syslog.error('SCRIPT : Show version failed')   
