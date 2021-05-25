"""
This script changes the hostname to Demo.

How to run?
script run exec <path> test_netconf_config.py
eg: script run /harddisk\: test_netconf_config.py

Configuration: 
hostname Demo

Verify:
Check that hostname has changed
"""
import os
import netconf_test_common

from cisco.script_mgmt import xrlog

log = xrlog.getScriptLogger('test_netconf_config')
syslog = xrlog.getSysLogger('test_netconf_config')
LOG_FILE = "netconf_oper_1_" + str(os.getpid()) + ".txt"

def config_hostname():
    """
    Configure hostname
    """
    logfile = netconf_test_common.DEFAULT_LOG_PATH + LOG_FILE
    edit_config = """
        <host-names xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg">
            <host-name>Demo</host-name>
        </host-names>"""
    try:
        netconf_test_common.logf = open(logfile, 'w')
    except Exception as e:
        print("ERROR: Unable to open " + logfile + "!")
        return None
    # Initialize Netconf Connection
    nc = NetconfClient(debug=True)
    nc.connect()
    
    if netconf_test_common.do_edit_cfg(nc, config=edit_config):
        netconf_test_common.do_commit(nc)
 
    nc.close()
    netconf_test_common.logf.close()

if __name__ == '__main__':

    syslog.info('Changing hostname to demo')
    config_hostname()
