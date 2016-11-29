import os
import sys
import re
from process import Process

class Proc:
    def __init__(self):
        self.proc = '/proc/'
        self.processList = []
        self.totalMem = 0
        # Will hold our pids that are inside /proc/ as well as the process's information
        self.readData()

    def readData(self):
        self.readTotalMem()
        self.readProcListData()

    # FIXME: skip looping and try to acess directly
    def readTotalMem(self):
        fd = open(self.proc + "/meminfo")
        for i, line in enumerate(fd):
            if i == 0:
                items = line.split(" ")
                for j, item in enumerate(items):
                    if items[j].isdigit():
                        self.totalMem = int(items[j])
            else:
                break
        fd.close()

    # Collect PIDs and statuses from each pid
    def readProcListData(self):
        self.processList = []
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
                item = line.split(" ")
                process.name = item[1][1:-1]

                process.rss = item[23]
                process.ramPrecentage = int(process.rss)
                process.ramPrecentage = (process.ramPrecentage*4096)/1024
                process.ramPrecentage = process.ramPrecentage/self.totalMem
                process.ramPrecentage = process.ramPrecentage*100
                process.ramPrecentage = str(process.ramPrecentage)

                process.utime = item[15]
                process.stime = item[16]
            fd.close()
            self.processList.append(process)
