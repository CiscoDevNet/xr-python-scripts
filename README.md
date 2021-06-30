<!--
  Copyright (c) 2021 by Cisco Systems, Inc.
  All rights reserved.
-->
# Overview

OPS stands for operational simplicity which is achieved by "on-the-box" automation in python, on IOS-XR routers.

This feature is supported on IOS-XR releases 7.3.2 onwards.

There are 4 types of scripts:

## 1. Exec Script ##

An exec script is a script that gets triggered via a CLI or a rpc over netconf. The script should be able to do whatever a management script can do from an external controller: connect to netconf/gNMI server on the same box, configure the box, query oper data, all model based, or CLI driven (CLI driven only available via netconf connection). To get the yang models please refer to : https://github.com/YangModels/yang/tree/master/vendor/cisco/xr/731

## 2. Config Script ##

A config script is used to enforce that the router configuration adheres to one or more customer-defined constraints. It is triggered automatically during configuration commits, and may either reject the commit (if invalid) or make changes to the contents of the commit (to make the resulting configuration valid). This ability to modify the contents of the commit can also be used to effectively automate repetitive configuration tasks, by making additional config changes that relate to the changes originally in the commit.

## 3. EEM Script ##

The difference between an eem script and an exec script is that the eem script is triggered via a predefined set of events whereas the exec script is triggered by a CLI(user). In 7.4.1 and 7.3.2 IOS-XR releases, the only event that is supported is syslog. 7.5.1 onwards, we also have timer, track and telemetry events support along with logical correlation of events, rate-limit, occurrence and period. 

Every eem script has a maxrun (default is 20 seconds and can be overridden via config). If script doesn't terminate in "maxrun" time, script is killed.

## 4. Process Script: ##

The exec/eem/config scripts are transient in nature. In general, they start running due to an external trigger (a CLI, an event, a commit action), they run for a short period of time and they cease running. If these scripts cease running as part of normal code flow, or due to a mishap (it crashes itself, or some other processes kills it), no entity will attempt to run it again without next external trigger. If an exec/eem/config script does not cease once it starts running, no entity will attempt to stop it or kill it. The script is pretty much on its own with respect to “life cycle management.”

A process script is quite different as it will try to run forever as part of its design, and if it exits due to abnormal reason (it crashes itself, some other processes kill it, etc.), an external entity will try to restart the process. In another word, there is an external entity to do the “life cycle management” of the script.


# Getting Started

## Step 1 ##

Clone git repo: https://github.com/CiscoDevNet/iosxr-ops.git

## Step 2 ## 

Copy python files to router's harddisk or a tftp location

## Step 3 ##

Add script:

script add {config,eem,exec,process} {tftp:<path>,/harddisk:/<path>} \<filename\> [checksum \<value\>] [\<filename\> [checksum \<value\>] … ]

Two methods to add scripts to script management repository
  
### Method 1: ###
  
Script add using http 
  
Example:
  
	script add exec http://10.85.67.235/scripts exec_upgrade_check.py checksum 023aa948b76e4177e9decf16911eff04896809f70deaaae9161d1dd2761da297
  
### Method 2:  ###
  
Copy script to harddisk using scp/copy CLI.
  
Script add from harddisk
  
Example:
  
![image](https://user-images.githubusercontent.com/32883901/120832424-4317e280-c526-11eb-8b24-37db160e2879.png)


## Step 4 ##
Note: 

1. For eem script checksum is configured with the event manager action and details can be found in the eem string docstrings.

2. For config script user must commit the configuration "configuration validation scripts" before configuring a specific script. 

Checksum configuration is MANDATORY to run scripts
  
Syntax for exec, config and process script:
	config terminal
 		script {config,exec,process} <filename> checksum {sha256 <value>}
  
Example:
	
![image](https://user-images.githubusercontent.com/32883901/120832696-8eca8c00-c526-11eb-96e3-2704a20f7265.png)





## Step 5 ##

Check script status using the cli show script status. It should be "Ready"

```
RP/0/RP0/CPU0:ios#show script status 
Tue Jun 21 16:35:14.877 UTC
======================================================================================================
 Name                            | Type   | Status           | Last Action | Action Time               
------------------------------------------------------------------------------------------------------
 test_cli_config.py              | exec   | Ready            | NEW         | Tue Jun 21 16:32:57 2021  
======================================================================================================
RP/0/RP0/CPU0:ios#
```

To see more details:

```
RP/0/RP0/CPU0:ios#show script status detail 
Tue Jun 21 16:37:05.928 UTC
======================================================================================================
 Name                            | Type   | Status           | Last Action | Action Time               
------------------------------------------------------------------------------------------------------
 test_cli_config.py              | exec   | Ready            | NEW         | Tue Jun 21 16:32:57 2021  
------------------------------------------------------------------------------------------------------
 Script Name       : test_cli_config.py
 Checksum          : dcfad756c7d0e8a23782dc7a159179bb6226e1d4edd689f31457f405ff79b1a6
 History:
 --------
 1.   Action       : NEW
      Time         : Tue Jun 21 16:32:57 2021
      Checksum     : dcfad756c7d0e8a23782dc7a159179bb6226e1d4edd689f31457f405ff79b1a6
      Description  : User action IN_CLOSE_WRITE
======================================================================================================
RP/0/RP0/CPU0:ios#
```




