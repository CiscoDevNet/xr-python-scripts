"""
This script accepts configuration from the user and commits it to the router.

Pre-requisite configuration on router:
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

How to run?
script run exec <path> test_cli_config.py arguments <config>
eg: script run /harddisk\: test_cli_config.py arguments "hostname Demo"

Configuration: 
Provided by user as command line argument

Verify:
check for syslog: 'SCRIPT : Configuration succeeded'
""" 
import argparse
from iosxr.xrcli.xrcli_helper import XrcliHelper
from cisco.script_mgmt import xrlog

logger = xrlog.getScriptLogger('xr_cli_config')
syslog = xrlog.getSysLogger('xr_cli_config')
helper = XrcliHelper(debug = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="Single line string representing an XR config command",type=str)
    args = parser.parse_args()
    config = args.cmd
    result = helper.xr_apply_config_string(config)

    if result['status'] == 'success':
        syslog.info('SCRIPT : Configuration succeeded')
    else:
        syslog.error('SCRIPT : Configuration failed')
