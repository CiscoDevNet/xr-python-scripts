#!/pkg/bin/python3
# --------------------------------------------
# Shruti Rao
#
# Copyright (c) 2019-2020 by Cisco Systems, Inc.
# All rights reserved.
# --------------------------------------------
# - This script provides functions to invoke APIs and log results which are
# called by test scripts present in the directory

import traceback

DEFAULT_LOG_PATH = '/misc/disk1/'
MSG_SENT = '\n--------------- Sent to NETCONF agent ----------------'
MSG_RECIEVED = '\n----------- Received from NETCONF agent --------------'
MSG_SEPARATE = '------------------------------------------------------\n'

logf = None


def print_log(msg):
    global logf

    logf.write(msg)


def do_get_schema_list(nc):
    try:
        nc.rpc.schema_list()
    except Exception as e:
        print_log("Caught an Exception when retrieving schema list\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_edit_cfg(nc, config=None, path=None):
    try:
        if path is not None:
            nc.rpc.edit_config(file=path)
        elif config is not None:
            nc.rpc.edit_config(config=config)
        else:
            print_log("ERROR: Config data is empty!")
            return False
    except Exception as e:
        print_log("Caught an Exception when editing config\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False

    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)

    if "<ok/>" in nc.reply:
        return True
    else:
        return False


def do_commit(nc):
    try:
        nc.rpc.commit()
    except Exception as e:
        print_log("Caught Exception when committing config\n")
        print_log(traceback.print_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_discard(nc):
    try:
        nc.rpc.discard()
    except Exception as e:
        print_log("Caught Exception when discarding config\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_get(nc, filter=None, path=None):
    try:
        if path is not None:
            nc.rpc.get(file=path)
        elif filter is not None:
                nc.rpc.get(request=filter)
        else:
            print_log("ERROR: Get data is empty!\n")
            return False
    except Exception as e:
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        print_log("Caught an Exception when performing get\n")
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_lock(nc, datastore=None):
    try:
        if datastore:
            nc.rpc.lock(datastore=datastore)
        else:
            nc.rpc.lock()
    except Exception as e:
        print_log("Caught an Exception when locking datastore\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_unlock(nc, datastore=None):
    try:
        if datastore:
            nc.rpc.unlock(datastore=datastore)
        else:
            nc.rpc.unlock()
    except Exception as e:
        print_log("Caught an Exception when unlocking datastore\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_get_caps(nc):
    try:
        nc.rpc.capability_list()
    except Exception as e:
        print_log("Caught an Exception when fetching capability list\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_get_cfg(nc, filter=None, datastore=None, path=None):
    data = {}
    if datastore is not None:
        data["datastore"] = datastore
    if filter is not None:
        data["config_filter"] = filter
    if path is not None:
        data["file"] = path
    try:
        nc.rpc.get_config(**data)
    except Exception as e:
        print_log("Caught an Exception when performing get_config\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True


def do_validate(nc, config=None, path=None):
    data = {}
    if config is not None:
        data["config"] = config
    if path is not None:
        data["file"] = path
    try:
        nc.rpc.validate(**data)
    except Exception as e:
        print_log("Caught an Exception when performing validate\n")
        print_log(str(e) + "\n")
        print_log(traceback.format_exc())
        return False
    print_log(MSG_SENT)
    print_log(nc.request)
    print_log(MSG_SEPARATE)

    print_log(MSG_RECIEVED)
    print_log(nc.reply)
    print_log(MSG_SEPARATE)
    return True
