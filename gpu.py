from pynvml import *
import psutil
from datetime import datetime


class NvidiaClient():

    def __init__(self) -> None:
        nvmlInit()
        self.devices = [i for i in range(nvmlDeviceGetCount())]

    def __enter__(self):
        return self

    def get_usage(self):
        data = []
        for deviceIndex in self.devices:
            handle = nvmlDeviceGetHandleByIndex(deviceIndex)
            rates = nvmlDeviceGetUtilizationRates(handle)
            memory = nvmlDeviceGetMemoryInfo(handle)
            used_by = []
            for process in nvmlDeviceGetComputeRunningProcesses(handle):
                pid = process.pid
                for p in psutil.process_iter():
                    if p.pid ==pid:
                        proc = p
                        break
                obj = {
                    "name": proc.name(),
                    "username": proc.username(),
                    "pid": pid,
                    "started_timestmap": proc.create_time(),
                    "started":  datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                    "cmdline": proc.cmdline(),
                    "gpu_memory": process.usedGpuMemory
                }
                used_by.append(obj)
            data.append({
                "index":deviceIndex,
                "name": str(nvmlDeviceGetName(handle),encoding="utf-8"),
                "gpu":rates.gpu,
                "memory":{
                    "total":memory.total,
                    "used":memory.used,
                    "free":memory.free,
                    "rate":memory.used/memory.total
                },
                "used_by":used_by
            })
        return data

    def __exit__(self,type, value, trace):
        nvmlShutdown()

    def __del__(self):
        nvmlShutdown()

if __name__=="__main__":
    client = NvidiaClient()
    print(client.get_usage())

