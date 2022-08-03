"""
Config script to check if certain ospf characteristics match desired values

"""


import cisco.config_validation as xr

from cisco.script_mgmt import xrlog

syslog = xrlog.getSysLogger('check_ospf')

#These values should be adjusted as seen fit
area_to_check = 0
process_name = "100"
interface_name = "TenGigE0/0/0/2"
hello_interval_req = 30
cost_minimum = 5

def check_ospf(root):

	#The ospf area to check
	area = root.get_node("/ipv4-ospf-cfg:ospf/processes/process[process-name='%s']/default-vrf/area-addresses/area-area-id[area-id=%i]" %(process_name, area_to_check))	
	
	#If the area exists
	if area:
		syslog.info("Area %s found" %area_to_check)

		#The given interface to check
		interface = area.get_node("/name-scopes/name-scope[interface-name='%s']" %interface_name)
		if interface:
			syslog.info("Interface %s found" %interface_name)
			
			#Get the leaf node representing the cost of the path
			curr_cost = interface.get_node("/cost")

			#If the cost has been previously set
			if curr_cost:
				syslog.info("Current cost is %s" %curr_cost.value)

				#Check to see if the cost is less than the minimum	
				if curr_cost.value < cost_minimum:
					xr.add_error(curr_cost, "Cost cannot be lower than %s" %cost_minimum) #Throw error
			
			#Get the leaf node representing the hello interval
			curr_hello_interval = interface.get_node("/hello-interval")
			if curr_hello_interval:
				syslog.info("Current hello interval is %s seconds" %curr_hello_interval.value)

				#Check the value of the hello interval
				if curr_hello_interval.value != hello_interval_req:
					curr_hello_interval.set_node(None, hello_interval_req) #set the hello interval
					syslog.info("Hello interval set to %s seconds" %hello_interval_req)

			#If the hello interval isn't previosly set
			else:
				syslog.info("No hello interval set previously, now set to %s seconds" %hello_interval_req)
				interface.set_node("/hello-interval", hello_interval_req) #set the hello interval
			

#Only run the script if an ospf process is changed
xr.register_validate_callback(["/ipv4-ospf-cfg:ospf/processes/*"], check_ospf)
