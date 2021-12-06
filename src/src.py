import psutil as ps
from pprint import pprint

def cpu_monitoring():
    cpu_counter = ps.cpu_count()
    cpu_freq = ps.cpu_freq()
    cpu_usage = ps.cpu_percent()
    cpu_info_dict = {
        "cpu_count": cpu_counter,
        "current_frequency": cpu_freq[0],
        "min_frequency": cpu_freq[1],
        "max_frequency": cpu_freq[2],
        "cpu_usage_%": cpu_usage
    }
    return cpu_info_dict
 
def show(**kwargs):
    cpu = cpu_monitoring

def run():
    ...

pprint(cpu_monitoring())