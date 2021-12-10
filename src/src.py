import psutil as ps
import json
from os import close, system
from datetime import datetime
from functools import wraps


def json_decorator(func):
    @wraps(func)
    def wrapper():
        json_dict = {}
        key = func.__name__.split("_")[0]
        json_dict[key] = func()
        date = datetime.now()
        with open(f'{date.strftime("%d_%b_%Y_%H_%M_%S")}.json', "a") as file:
            file.write(json.dumps(json_dict, indent=4))
        return func()
    return wrapper


@json_decorator
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


@json_decorator
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


@json_decorator
def disk_monitoring():
    disk_info = ps.disk_partitions()
    disk_info_dict = {}
    for disk in disk_info:
        disk_path = disk[0][0]
        disk_info_dict[f"disk_{disk_path}_type"] = disk[2]
        disk_info_dict[f"disk_{disk_path}_permissions"] = disk[3]
    return disk_info_dict

 
@json_decorator
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


def run():
    show_template(cpu = cpu_monitoring(), 
                  memory = memory_monitoring(),
                  disk = disk_monitoring(),
                  net = net_monitoring()
    )
    

if __name__ == '__main__':
    run()


    





