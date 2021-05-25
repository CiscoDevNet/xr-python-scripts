"""
This script is trigged when a process restart syslog is found and it prints which process is restarted

Required configuration:
username eem_user1
group root-lr
group cisco-support
!
aaa authorization exec default group tacacs+ local
aaa authorization eventmanager default local
aaa authentication login default group tacacs+ local

event manager event-trigger trigger1
type syslog pattern "PROC_RESTART_NAME"

event manager action action1
username eem_user1
type script script-name test_eem.py maxrun seconds 60 checksum disable

event manager policy-map policy1
trigger event trigger1
action action1

To verify:
Check for syslog EVENT SCRIPT EXECUTED: User restarted <process_name>

"""
from cisco.script_mgmt import xrlog
from iosxr import eem
import re

syslog = xrlog.getSysLogger("test_eem")
rc, event_dict = eem.event_reqinfo()
msg = event_dict['msg']
p=re.compile("process\s(\w+[a-zA-Z])")
process_name = p.search(msg).group()
syslog.info("EVENT SCRIPT EXECUTED: User restarted "+ process_name)
