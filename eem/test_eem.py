# Copyright (c) 2021 by Cisco Systems, Inc.
# All rights reserved.

"""
Sample EEM script

If a user restarts any process a syslog is generated. When syslog with "PROC_RESTART_NAME" is found the event script is triggered.
The script processes the event (syslog) and prints the name of the process restarted by the user.

Required configuration:
User and AAA configuration

event manager event-trigger <trigger-name>
type syslog pattern "PROC_RESTART_NAME"

event manager action <action-name>
username <user>
type script script-name <script-name> checksum sha256 <checksum>

event manager policy-map policy1
trigger event <trigger-name>
action <action-name>

To verify:
Check for syslog EVENT SCRIPT EXECUTED: User restarted <process-name>

"""
from cisco.script_mgmt import xrlog
from iosxr import eem
import re

syslog = xrlog.getSysLogger("test_eem")

rc, event_dict = eem.event_reqinfo()
# event_dict consists of details of the syslog

msg = event_dict['msg']
p=re.compile("process\s(\w+[a-zA-Z])")
process_name = p.search(msg).group()
syslog.info("EVENT SCRIPT EXECUTED: User restarted "+ process_name)
