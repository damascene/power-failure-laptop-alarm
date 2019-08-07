#!/usr/bin/env python3
# Built on https://askubuntu.com/a/519045
#License: GPL v 3.0
#Copyrigt: Damascene

# Works on Linux, Tested on Ububntu 16.04
# ssmtp package could be used and configured for email notfications functionality

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
    It checks the adaptor status every 10 seconds.
    When a change does happen it reprots it.
    """
    # the two commands to run if adapter is connected or not
    # Uncomment the following two line to enable email notification
    # command_on = '''echo "POWER ALERT - ON" | mail -s "POWER ALERT - ON" maile@example.com'''
    # command_off = '''echo "POWER ALERT - OFF" | mail -s "POWER ALERT - OFF" maile@example.com'''
    command_on = "notify-send On-line"
    command_off = "notify-send Off-line"
    last = "on"
    # open file for writig in append mode and create if not exist (a+)
    f= open("power.log","a+")
    while True:
        charge = str(read_status())
        if charge == "on-line":
            if last == "off":
                f.write("\nPower ON, "+time.strftime('%d-%m-%Y %H:%M:%S'))      #save data to a log file with timestamp
                # commit data to file so it shows in tail 
                f.flush()
                subprocess.Popen(["/bin/bash", "-c", command_on])
                last = "on"
        elif charge == "off-line":
            if last == "on":
                f.write("\nPower OFF, "+time.strftime('%d-%m-%Y %H:%M:%S'))     #save data to a log file with timestamp
                # commit data to file so it shows in tail
                f.flush()
                subprocess.Popen(["/bin/bash", "-c", command_off])
                last = "off"
        else:
            raise ValueError("impossible")
        time.sleep(10)

take_action()
