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

    from hardware-info import get_cpu_usage
    from evaluator import evaluate
    from notifier import send_mail
   
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
