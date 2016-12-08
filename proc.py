import os
import sys
import re
import errno # Need this for comparing exception errors and seeing what type they are
import subprocess # For readOpenWindow()
from process import Process
from cpu import CPU
from userlist import UserList

class Proc:
    def __init__(self):
        self.proc = '/proc/'
        self.processList = {} # Make a dictionary which is a hashtable
        self.cpu = [] # cpu[0] should be the collective info on all CPUs
        self.totalMem = 0
        self.userList = UserList()
        # Will hold our pids that are inside /proc/ as well as the process's information
        self.readData()

    def readData(self):
        self.userList = UserList() # Update our user list, never know if a new user is constructed
        self.readTotalMem()
        self.readcpuTimes()
        self.readProcListData()
        self.readOpenWindows()

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
        if len(self.cpu) != 0:
            bufcpu[0].period = bufcpu[0].period - self.cpu[0].period
        self.cpu = bufcpu

    # Collect PIDs and statuses from each pid
    def readProcListData(self):
        bufprocessList = {}
        debug = False # Incase we need to check our calculations
        if debug:
            print("-----------------------------------")
            print("            Start of loop          ")
            print("-----------------------------------")
        for pid in os.listdir(self.proc):
            process = Process()
            if not pid.isdigit():
                continue
            process.pid = pid
            process.ramPercentage = 0
            fd = open(self.proc + pid + "/status")
            for i, line in enumerate(fd):
                if debug:
                    print("({}) = {}, i={}".format(i+1,line,i))
                if i == 7:
                    item = re.split("[\t ]+", line)
                    process.realUid = int(item[1])
            fd.close()
            if debug:
                print("UID = {}".format(process.realUid))
            fd = open(self.proc + pid + "/stat")
            for i, line in enumerate(fd):
                # item = line.split(" ") # OLD
                item = re.split("[\t ]+", line)
                if debug:
                    for x, iter in enumerate(item):
                        print("({}) = {}, x={}".format(x+1,iter,x))
                process.name = item[1][1:-1]
                process.state = item[2]
                process.setFullState()

                process.rss = item[23]
                process.ramPercentage = int(process.rss)
                process.ramPercentage = (process.ramPercentage*4096)/1024
                process.ramPercentage = process.ramPercentage/self.totalMem
                process.ramPercentage = process.ramPercentage*100
                # Clamp 0 to 100
                process.ramPercentage = max(0, min(process.ramPercentage, 100))
                process.ramPercentage = "{:.2f}".format(process.ramPercentage)

                process.utime = int(item[13])
                process.stime = int(item[14])
                if debug:
                    print("PID {} == {} item[0]".format(pid,item[0]))
                    print("RSS: {}".format(process.rss))

                # Did the process exist already from last scan? Setup proper interval for calculation
                lp = self.processList.get(pid)
                if lp is None:
                    lastTimes = 0
                else:
                    lastTimes = lp.utime + lp.stime
                process.cpuPercentage = (process.utime + process.stime - lastTimes) / self.cpu[0].period * 100
                # Clamp 0 to 100
                process.cpuPercentage = max(0, min(process.cpuPercentage, 100))
                process.cpuPercentage = "{:.2f}".format(process.cpuPercentage)
                if debug:
                    print("PID: {}, {}% = ({} + {} - {}) / {} * 100".format(process.pid,process.cpuPercentage, process.utime, process.stime, lastTimes, self.cpu[0].period))
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
        if debug:
            print("-----------------------------------")
            print("            End of loop            ")
            print("-----------------------------------")

    def readOpenWindows(self):
        ret = subprocess.run(['wmctrl', '-lp'],stdout=subprocess.PIPE,universal_newlines=True)
        lines = re.split("(.+)\n", ret.stdout)
        for line in lines:
            # Split up the fields for each line
            fields = re.match("(\w+)\s+(\w+)\s+(\w+)\s+(.[^\s]+)\s+(.+)", line)
            if fields is not None:
                pid = fields.group(3)
                windowName = fields.group(5)
                process = self.processList.get(pid)
                if process is not None:
                    process.windowName = windowName

# FIXME: Delete when done project
# For testing proc.py's data gathering
if __name__ == "__main__":
    proc = Proc()
    proc.readData()
