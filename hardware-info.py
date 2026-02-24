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
