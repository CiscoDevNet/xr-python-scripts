# OPS1.0

OPS stands for operational simplicity which is achieved by "on-the-box" automation in python, on IOS-XR routers.

There are 4 types of scripts:

## 1. Exec Script ##

An exec script is a script that gets triggered via a CLI or a rpc over netconf. The script should be able to do whatever a management script can do from an external controller: connect to netconf/gNMI server on the same box, configure the box, query oper data, all model based, or CLI driven (CLI driven only available via netconf connection).

## 2. Config Script ##

Commit script is a script that gets triggered during a “commit” process. When a configuration commit is going on, a “commit script” inserts itself into the commit process as a “middle-end” management agent. 

## 3. EEM Script ##

The difference between an eem or event script and an exec script is that the eem script is triggered via a predefined set of events whereas the exec script is triggered by a CLI(user). Only event currently supported is a syslog.

## 4. Process Script: ##

The exec/eem/config scripts are transient in nature. In general, they start running due to an external trigger (a CLI, an event, a commit action), they run for a short period of time and they cease running. If these scripts cease running as part of normal code flow, or due to a mishap (it crashes itself, or some other processes kills it), no entity will attempt to run it again without next external trigger. If an exec/eem/config script does not cease once it starts running, no entity will attempt to stop it or kill it. The script is pretty much on its own with respect to “life cycle management.”

A process script is quite different as it will try to run forever as part of its design, and if it exits due to abnormal reason (it crashes itself, some other processes kill it, etc.), an external entity will try to restart the process. In another word, there is an external entity to do the “life cycle management” of the script.
