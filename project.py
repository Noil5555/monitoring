import psutil
import platform
import time
from datetime import datetime
import system_info
import smtplib
from email.mime.text import MIMEText



uname = platform.uname()
cpufequence = psutil.cpu_freq()
svmem = psutil.virtual_memory()
partitions = psutil.disk_partitions()
if_addrs = psutil.net_if_addrs()
net_io = psutil.net_io_counters()
sender = "a-mail@info.com"
adresser = "you-mail@gmail.com"
cpu_logging = ""
cpu_status = ""
ram_logging = ""
ram_status = ""
disk_logging = ""
disk_status = ""

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def cpu_hermpf():
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
    if cpu_usage.total <= 80:
        cpu_status = "Okay"
    elif cpu_usage.total >= 80:
        cpu_status = "Warning"
    elif cpu_usage.total >= 90:
        cpu_status = "Critical"
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

       

    time.sleep(300)
