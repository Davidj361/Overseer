import os
import sys
import re
from process import Process
from cpu import CPU

class Proc:
    def __init__(self):
        self.proc = '/proc/'
        self.processList = {} # Make a dictionary which is a hashtable
        self.cpu = [] # cpu[0] should be the collective info on all CPUs
        self.totalMem = 0
        # Will hold our pids that are inside /proc/ as well as the process's information
        self.readData()

    def readData(self):
        self.readTotalMem()
        self.readcpuTimes()
        self.readProcListData()

    # FIXME: skip looping and try to acess directly
    def readTotalMem(self):
        fd = open(self.proc + "/meminfo")
        for i, line in enumerate(fd):
            if i == 0:
                # items = line.split(" ") # OLD
                items = re.split("[\t ]+", line)
                for j, item in enumerate(items):
                    if items[j].isdigit():
                        self.totalMem = int(items[j])
            else:
                break
        fd.close()
        
    # FIXME: skip looping and try to acess directly
    def readcpuTimes(self):
        fd = open(self.proc + "/stat")
        bufcpu = []
        for i, line in enumerate(fd):
            # What it looks like for the first line: cpu  67188 150 8766 5124308 14884 0 711 0 0 0
            # Keep checking until cpu isn't the first word so we collected all times for CPUs
            if re.match("^cpu",line) != None:
                items = re.split("[\t ]+", line)
                cpu = CPU(items[1],items[2],items[3],items[4],items[5],items[6],items[7],items[8])
                bufcpu.append(cpu)
            else:
                break
        fd.close()
        # Get our interval from last scan
        self.cpu = bufcpu

    # Collect PIDs and statuses from each pid
    def readProcListData(self):
        bufprocessList = {}
        for pid in os.listdir(self.proc):
            process = Process()
            if not pid.isdigit():
                continue
            fd = open(self.proc + pid + "/stat")
            process.item = ""
            process.pid = pid
            process.name = ""
            process.rss = ""
            process.utime = ""
            process.stime = ""
            process.ramPrecentage = 0
            for i, line in enumerate(fd):
                # item = line.split(" ") # OLD
                item = re.split("[\t ]+", line)
                process.name = item[1][1:-1]

                process.rss = item[23]
                process.ramPrecentage = int(process.rss)
                process.ramPrecentage = (process.ramPrecentage*4096)/1024
                process.ramPrecentage = process.ramPrecentage/self.totalMem
                process.ramPrecentage = process.ramPrecentage*100
                process.ramPrecentage = str(process.ramPrecentage)

                process.utime = item[15]
                process.stime = item[16]

                # lastTimes = 0
                # process.cpuPrecentage = (process.utime + process.stime - lastTimes)
            fd.close()
            bufprocessList[pid] = process
        self.processList = bufprocessList


# FIXME: Delete when done project
# For testing proc.py's data gathering
if __name__ == "__main__":
    proc = Proc()
    for iter in proc.cpu:
        print(iter.totaltime)
