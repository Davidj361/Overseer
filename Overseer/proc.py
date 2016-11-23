import os
import sys
import re

class Proc:
    def __init__(self):
        self.proc = '/proc/'
        self.data = []
        # Will hold our pids that are inside /proc/ as well as the process's information
        self.getData()

    # Collect PIDs and statuses from each pid
    def getData(self):
        self.data = []
        for element in os.listdir(self.proc):
            if not element.isdigit():
                continue
            # element = int(element) # might not be needed
            fd = open(self.proc + element + "/status")
            for i, line in enumerate(fd):
                if i == 0:
                    matchObj = re.search("^Name:\s*(.*)$", line)
            fd.close()
            self.data.append([element,matchObj.group(1)])
            print(self.data)

# FIXME : DELETEME
proc = Proc()

#subprocess.call(["cat", "/proc/meminfo"])
