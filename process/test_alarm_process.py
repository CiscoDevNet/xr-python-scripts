"""
Process script to monitor the number of alarms present on the router

Email notification will be sent when this number changes using Cisco SMTP server

Must be connected to Cisco network for emailing capabilities to function properly

To trigger script
Step 1: Add and configure script as shown in README.MD

Step 2: Register the application with Appmgr

Configuraton:
appmgr process-script my-process-app
executable test_process.py
run-args <threshold-value>

Step 3: Activate the registered application
appmgr process-script activate name my-process-app

"""



import time 
import os
import xmltodict
import re


#For emailing functions
import smtplib as SMTP
from email.mime.text import MIMEText

#For logging
from cisco.script_mgmt import xrlog
from iosxr.netconf.netconf_lib import NetconfClient

log = xrlog.getScriptLogger('Alarm')
syslog = xrlog.getSysLogger('Alarm')

def check_curr_alarm_num(prev_count):
	"""
	Checks current number of alarms
	"""
	curr_count = 0
	filter_string = """
	<alarms xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-alarmgr-server-oper">
		<detail>
			<detail-system>
				<stats>
					<reported/>
				</stats>
			</detail-system>
		</detail>
	</alarms>"""

	nc = NetconfClient(debug=True)
	nc.connect() #Connects the NetconfClient
	do_get(nc, filter=filter_string) #Makes a Netconf get call
	ret_dict = _xml_to_dict(nc.reply, 'alarms') #Parses the data from the Netconf Reply into a dictionary format for easy retrieval
	curr_count = int(ret_dict['alarms']['detail']['detail-system']['stats']['reported']) #Retrieves number of alamrs from the created dictionary
	count_file = open("count.txt", "wt") 
	count_file.write("Current number of alarms: %s \n" %curr_count) #Writes number of alarms to file
	count_file.close()
	if curr_count != prev_count: #Checks number of alarms compared to previous number
		syslog.error("New Alarm Detected: new count = %s, old count = %s" %(curr_count, prev_count)) #If the number is different, print a syslog error
		_send_email(curr_count, prev_count) #Send an email notifying network monitor
	nc.close() #Close the Netconf client


def _send_email(curr_count, prev_count):
    SMTP_server = 'outbound.cisco.com' 
    sender = 'epickhar@cisco.com'
    dest = 'epickhar@cisco.com'

    text_subtype = 'plain'


    #Email contents
    content = """\
	NEW ALARM DETECTED: NEW COUNT = %s, OLD COUNT = %s
	""" %(curr_count, prev_count)

    subject = "Alarm Change Detected"
    msg = MIMEText(content, text_subtype)
    msg['Subject'] = subject
    msg['From'] = sender

    #Connect to SMTP server with port number
    conn = SMTP.SMTP(SMTP_server, 25)
    conn.set_debuglevel(False)

    #Send email
    try:
        conn.sendmail(sender, dest, msg.as_string())
    except:
        syslog.error("Message Failed to Send")
    finally:
        conn.quit()

def _xml_to_dict(xml_output, xml_tag=None):
	"""
	convert netconf rpc request to dict
	:param xml_output:
	:return:
	"""
	if xml_tag:
		pattern = "<data>\s+(<%s.*</%s>).*</data>" % (xml_tag, xml_tag)
	else:
		pattern = "(<data>.*</data>)"
	xml_output = xml_output.replace('\n', ' ')
	xml_data_match = re.search(pattern, xml_output)
	ret_dict = xmltodict.parse(xml_data_match.group(1))
	return ret_dict

def do_get(nc, filter=None, path=None):
	"""
	makes netconf rpc get request
	:param nc: Netconf client
	:return bool if request successful:
	"""
	try:
		if path is not None:
			nc.rpc.get(file=path)
		elif filter is not None:
			nc.rpc.get(request=filter)
		else:
			return False
	except Exception as e:
			return False
	return True

if __name__ == '__main__':
	prev_count = 0
	while(1): #Process script, run continuously
		check_curr_alarm_num(prev_count)
		count_file = open("count.txt", "rt") #Get the previous count from the file
		prev_count = int(count_file.readline()[26:]) #Parse data
		count_file.close() #Close file
		time.sleep(60) #Run every minute
