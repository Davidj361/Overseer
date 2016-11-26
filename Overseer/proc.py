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
        totalMem = 0
        fd = open(self.proc + "/meminfo")
        for i, line in enumerate(fd):
            if i == 0:
                items = line.split(" ")
                for j, item in enumerate(items):
                    if items[j].isdigit():
                        totalMem = int(items[j])
            else:
                break
        fd.close()
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
                rssNum = int(rss)
                rssNum = (rssNum*4096)/1024
                rssNum = rssNum/totalMem
                rssNum = rssNum*100
                rss = str(rssNum)
            fd.close()
            self.data.append([name, pid, "user", "", rss])
