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
        for pid in os.listdir(self.proc):
            if not pid.isdigit():
                continue
            # pid = int(pid) # might not be needed
            #old, using status, not stat
            """
            fd = open(self.proc + pid + "/status")
            for i, line in enumerate(fd):
                if i == 0:
                    matchName = re.search("^Name:\s*(.*)$", line)
            fd.close()
            self.data.append([matchName.group(1),pid, "user"])
            """
            fd = open(self.proc + pid + "/stat")
            item = ""
            name = ""
            rss = ""
            for i, line in enumerate(fd):
                item = line.split(" ")
                name = item[1][1:-1]
                rss = item[23]
                rssInt = int(rss)
                rss = str(rssInt*4096)
            fd.close()
            self.data.append([name, pid, "user", "", rss])
