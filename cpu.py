class CPU:
    # Note: Guest and Guest_nice are already accounted in user and nice, hence they are not included in the total calculation
    def __init__(self):
        self.usertime = 0 # user   (1) Time spent in user mode.
        self.nicetime = 0 # nice   (2) Time spent in user mode with low priority (nice).
        self.systime = 0 # system (3) Time spent in system mode.
        self.idletime = 0 # idle   (4) Time spent in the idle task.  This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
        self.iotime = 0 # iowait (since Linux 2.5.41) (5) Time waiting for I/O to complete.
        self.irqtime = 0 # irq (since Linux 2.6.0-test4) (6) Time servicing interrupts.
        self.softirqtime = 0 # softirq (since Linux 2.6.0-test4) (7) Time servicing softirqs.
        self.stealtime = 0 # steal (since Linux 2.6.11) (8) Stolen time, which is the time spent in other operating systems when running in a virtualized environment
        # Period will be our delta times from the last scan
        self.period = 0
    def __init__(self, usertime, nicetime, systime, idletime, iotime, irqtime, softirqtime, stealtime):
        self.usertime = int(usertime) # user   (1) Time spent in user mode.
        self.nicetime = int(nicetime) # nice   (2) Time spent in user mode with low priority (nice).
        self.systime = int(systime) # system (3) Time spent in system mode.
        self.idletime = int(idletime) # idle   (4) Time spent in the idle task.  This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
        self.iotime = int(iotime) # iowait (since Linux 2.5.41) (5) Time waiting for I/O to complete.
        self.irqtime = int(irqtime) # irq (since Linux 2.6.0-test4) (6) Time servicing interrupts.
        self.softirqtime = int(softirqtime) # softirq (since Linux 2.6.0-test4) (7) Time servicing softirqs.
        self.stealtime = int(stealtime) # steal (since Linux 2.6.11) (8) Stolen time, which is the time spent in other operating systems when running in a virtualized environment
        # Period will be our delta times from the last scan
        self.period = self.usertime + self.nicetime + self.systime + self.idletime + self.iotime + self.irqtime + self.softirqtime + self.softirqtime + self.stealtime
