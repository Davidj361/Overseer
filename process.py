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

    # Force kill the process
    def endProcess(self):
        # Since the user field is still not implemented for the process, we'll just use another way of seeing if the user owns this file or not
        if self.pid != 0 and self.path != "DENIED":
            subprocess.run(['kill', '-9', self.pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return 0
        else:
            return 1 # Indicate an error
