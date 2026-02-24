import psutil
import platform
import system_info
import time
from datetime import datetime
import json
from pathlib import Path
import smtplib
from email.mime.text import MIMEText

CONFIG_PATH = Path("config.json")

if not CONFIG_PATH.exists():
    print("Could not find config.json. Make sure it is in the same diractory as the project.py skript")

with open (CONFIG_PATH , "r", encoding = "utf-8") as f:
    config = json.load(f)

uname = platform.uname()
cpufequence = psutil.cpu_freq()
svmem = psutil.virtual_memory()
partitions = psutil.disk_partitions()
if_addrs = psutil.net_if_addrs()
net_io = psutil.net_io_counters()
sender = config ["sender"]
adresser = config ["adresser"]
cpu_logging = ""
cpu_status = ""
ram_logging = ""
ram_status = ""
disk_logging = ""
disk_status = ""


def cpu_notification():
    if cpu_logging == "":
        cpu_logging = cpu_status
    elif cpu_logging != cpu_status:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Monitoring Warning CPU '+ cpu_logging
        msg['Von'] = sender
        msg['An'] = adresser

        s = smtplib.SMTP('localhost')
        s.sendmail(sender, [adresser], msg.as_string())
        s.quit()

        cpu_logging = cpu_status
    else:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Somthing want wrong'
        msg['Von'] = sender
        msg['An'] = adresser


while True:


    ##################################################################################
    # System-Info
    ##################################################################################

    sys_info = {
        "System": uname.system,
        "Nodes": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor,
    }

    ##################################################################################
    # CPU-Info
    ##################################################################################

    cpu_frequence = {
        "Max": cpufequence.max,
        "Min": cpufequence.min,
        "Current": psutil.cpu_freq,
    }

    cpu_usage = {
        "per_core": psutil.cpu_percent(interval=1, percpu=True),
        "total": psutil.cpu_percent(),
    }

    ##################################################################################
    # RAM-Info
    ##################################################################################

    ram_info = {
        "Total RAM": get_size(svmem.total),
        "Available RAM": get_size(svmem.available),
        "Used RAM": get_size(svmem.used),
        "Percentage RAM": {get_size(svmem.percent)},
        "disk": {},
        "network": {},
        "warnings": {},
    }

    ##################################################################################
    # Disk-Info
    ##################################################################################

    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)

            system_info["disk"][partition.device] = {
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": get_size(partition_usage.total),
                "used": get_size(partition_usage.used),
                "free": get_size(partition_usage.free),
                "percentage": partition_usage.percent,
            }

        except PermissionError:
            continue

    disk_io = psutil.disk_io_counters()

    system_info["disk"]["io"] = {
        "total_read": get_size(disk_io.read_bytes),
        "total_write": get_size(disk_io.write_bytes),
    }

    ##################################################################################
    # Warnings
    ##################################################################################

    # CPU Warning
    if cpu_usage["total"] >= 90:
        cpu_status = "Critical"
    elif cpu_usage["total"] >= 80:
        cpu_status = "Warning"
    elif cpu_usage["total"] <= 80:
        cpu_status = "Okay"
    else:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Unable to read CPU status' 
        msg['Von'] = sender
        msg['An'] = adresser

        s = smtplib.SMTP('localhost')
        s.sendmail(sender, [adresser], msg.as_string())
        s.quit()
        break
    
    cpu_notification()
       

    time.sleep(300)
