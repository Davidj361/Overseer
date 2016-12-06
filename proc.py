import os
import sys
import re
import errno # Need this for comparing exception errors and seeing what type they are
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
        # if len(self.cpu) != 0:
        #     bufcpu[0].period = bufcpu[0].period - self.cpu[0].period
        self.cpu = bufcpu

    # Collect PIDs and statuses from each pid
    def readProcListData(self):
        bufprocessList = {}
        for pid in os.listdir(self.proc):
            process = Process()
            if not pid.isdigit():
                continue
            process.pid = pid
            process.ramPercentage = 0
            fd = open(self.proc + pid + "/stat")
            for i, line in enumerate(fd):
                # item = line.split(" ") # OLD
                item = re.split("[\t ]+", line)
                process.name = item[1][1:-1]

                process.rss = item[23]
                process.ramPercentage = int(process.rss)
                process.ramPercentage = (process.ramPercentage*4096)/1024
                process.ramPercentage = process.ramPercentage/self.totalMem
                process.ramPercentage = process.ramPercentage*100
                process.ramPercentage = str(process.ramPercentage)

                process.utime = int(item[15])
                process.stime = int(item[16])

                # Did the process exist already from last scan? Setup proper interval for calculation
                lp = self.processList.get(pid)
                # FIXME: There's a problem here when using sleep(1)
                if lp is None:
                    lastTimes = 0
                else:
                    lastTimes = lp.utime + lp.stime
                process.cpuPercentage = (process.utime + process.stime - lastTimes) / self.cpu[0].period * 100
            fd.close()
            # Get the path of the program
            try:
                process.fullpath = os.readlink(self.proc + pid + "/exe") # We use os.system instead of os.readlink because of permission problems and the readlink command handles it ok
            except PermissionError as err:
                process.fullpath = "DENIED" # Permission was denied to read /exe
            # Otherwise, something really bad happened
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            if process.fullpath != "DENIED":
                # strip the process name off the full path
                process.path = os.path.dirname(process.fullpath)
            else:
                process.path = "DENIED" # Permission was denied to read /exe

            bufprocessList[pid] = process
        self.processList = bufprocessList


# FIXME: Delete when done project
# For testing proc.py's data gathering
if __name__ == "__main__":
    proc = Proc()
    proc.readData()
