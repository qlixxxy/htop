import psutil as ps
from os import close, system
from datetime import datetime
import json


def json_decorator(func):
    def wrapper():
        result_tuple = func()
        json_dict = {}
        date = datetime.now()
        with open(f'{date.strftime("%d_%b_%Y_%H_%M_%S")}.json', "w") as file:
            for i in result_tuple:
                header = i.__name__.split("_")[0]
                json_dict[header] = i()
            file.write(json.dumps(json_dict, indent=4))
    return wrapper


def cpu_monitoring(): 
    cpu_counter = ps.cpu_count()
    cpu_freq = ps.cpu_freq()
    cpu_usage = ps.cpu_percent()
    cpu_info_dict = {
        "cpu_count": cpu_counter,
        "current_frequency": cpu_freq[0],
        "min_frequency": cpu_freq[1],
        "max_frequency": cpu_freq[2],
        "cpu_usage": f"{cpu_usage} %"
    }
    return cpu_info_dict


def memory_monitoring():
    memory_info = ps.virtual_memory()
    bytes_per_mb = 1048576
    memory_info_dict = {
        "total_memory": f"{memory_info[0] / bytes_per_mb} MB",
        "available_memory": f"{memory_info[1] / bytes_per_mb} MB",
        "memory_usage": f"{memory_info[2]} %",
        "used_memory": f"{memory_info[3] / bytes_per_mb} MB"
    }
    return memory_info_dict


def disk_monitoring():
    disk_info = ps.disk_partitions()
    disk_info_dict = {}
    for disk in disk_info:
        disk_path = disk[0][0]
        disk_info_dict[f"disk_{disk_path}_type"] = disk[2]
        disk_info_dict[f"disk_{disk_path}_permissions"] = disk[3]
    return disk_info_dict

 
def net_monitoring():
    net_info = ps.net_io_counters()
    bytes_per_mb = 1048576
    net_info_dict = {
        "total_mb_sent": f"{net_info[0] / bytes_per_mb} MB",
        "total_mb_received": f"{net_info[1] / bytes_per_mb} MB",
        "packets_sent": net_info[2],
        "packets_received": net_info[3],
        "received_errors_number": net_info[4],
        "sent_errors_number": net_info[5]
    }
    return net_info_dict


def show_template(**kwargs):
    print("\n|-------CPU------|\n")
    iterable_dict(kwargs['cpu'])
    print("\n|-------MEMORY-------|\n")
    iterable_dict(kwargs['memory'])
    print("\n|-------DISKS-------|\n")
    iterable_dict(kwargs['disk'])
    print("\n|-------CONNECTIONS-------|\n")
    iterable_dict(kwargs['net'])
    

def iterable_dict(dict):
    for key, value in dict.items():
        print(f'{key}:   {value}')

@json_decorator
def to_json():
    return cpu_monitoring, memory_monitoring, disk_monitoring, net_monitoring


def run(is_json_needed = False):
    if is_json_needed:
        to_json()
    show_template(cpu = cpu_monitoring(), 
                  memory = memory_monitoring(),
                  disk = disk_monitoring(),
                  net = net_monitoring()
    )
    

if __name__ == '__main__':
    run(is_json_needed=True)


    





