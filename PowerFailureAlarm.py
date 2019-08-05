#!/usr/bin/env python3
# Built on https://askubuntu.com/a/519045
#License: AGPL v 3.0
#Copyrigt: Damascene

import subprocess
import time

def read_status():
    """
    This function get the status of acpi adapter from the laptop
    """
    command = "acpi -a | cut -d:  -f2 |sed 's/ //'"
    get_batterydata = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE)
    return get_batterydata.communicate()[0].decode("utf-8").replace("\n", "")

def take_action():
    """
    When the adaptor is connected, I assume the action does
    not have to be repeated every 10 seconds. As it is, it only runs
    1 time if status fliped.
    """
    # the two commands to run if adapter is connected or not
    command_on = "notify-send On-line"
    command_off = "notify-send Off-line"
    last = "on"
    while True:
        charge = str(read_status())
        if charge == "on-line2":
            if last == "off":
                subprocess.Popen(["/bin/bash", "-c", command_on])
                last = "on"
        elif charge == "off-line2":
            if last == "on":
                subprocess.Popen(["/bin/bash", "-c", command_off])
                last = "off"
        else:
            raise ValueError("impossible")
        time.sleep(10)

take_action()
