import subprocess

class Process:
    def __init__(self):
        self.name = ""
        self.fullname = ""
        self.fullpath = ""
        self.path = ""
        self.pid = 0
        self.rss = ""
        self.utime = ""
        self.stime = ""
        self.ramPercentage = 0
        self.cpuPercentage = 0
        self.realUid = 0
        self.state = ""
        self.fullState = ""
        self.windowName = ""

    # Force kill the process
    def endProcess(self):
        # Since the user field is still not implemented for the process, we'll just use another way of seeing if the user owns this file or not
        if self.pid != 0 and self.path != "DENIED":
            subprocess.run(['kill', '-9', self.pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return 0
        else:
            return 1 # Indicate an error

    # Force kill the child processes
    def endProcessTree(self):
        # Since the user field is still not implemented for the process, we'll just use another way of seeing if the user owns this file or not
        if self.endChildProcesses() == 0:
            return self.endProcess()
        else:
            return 1

    # Force kill the child processes
    def endChildProcesses(self):
        # Since the user field is still not implemented for the process, we'll just use another way of seeing if the user owns this file or not
        if self.pid != 0 and self.path != "DENIED":
            subprocess.run(['pkill', '-P', self.pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return 0
        else:
            return 1 # Indicate an error

    # Read 'man proc' and see /proc/[pid]/stat for more information
    def setFullState(self):
        if self.state == "R":
            self.fullState = "Running"
        elif self.state == "S":
            self.fullState = "Sleeping"
        elif self.state == "D":
            self.fullState = "Waiting"
        elif self.state == "Z":
            self.fullState = "Zombie"
        elif self.state == "T":
            self.fullState = "Stopped"
        elif self.state == "t":
            self.fullState = "Tracing stop"
        elif self.state == "W":
            self.fullState = "Waking or paging"
        elif self.state == "X":
            self.fullState = "Dead"
        elif self.state == "x":
            self.fullState = "Dead"
        elif self.state == "P":
            self.fullState = "Parked"
        else:
            self.fullState = ""
