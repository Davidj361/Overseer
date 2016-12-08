# Comp300Group5
### A task manager GUI application for Linux
### Created by: Trent McNabb & David Jatczak

![Alt text](preview1.png?raw=true)
![Alt text](preview2.png?raw=true)

# Requirements:
- Ubuntu 16.04 (Tested on)
- Python 3.5.2
- PyQt5
- wmctrl (Needed for seeing what windows are open on the linux window manager)

# To Run:
Clone or download the repository. Rename and move the repository folder as however you like.

Go into the main directory of the repository, type into terminal: python3 overseer.py

It should create a bash script as ~/openOverseer.sh, and you should get your logout shortcut disabled while 2 shortcuts are made in Ubuntu.

If you want to move the repository folder, just delete ~/openOverseer and the Overseer shortcuts and rerun overseer.py.

Note: Ctrl+Shift+Escape doesn't seem to work because shortcuts in Ubuntu with Escape just don't work.

# TODO LIST

## High Priority

- Go through all the code and fix the FIXME comments
- Add total CPU and RAM usage at the bottom of the window
- Give the program an icon

## Medium Priority

- Have the sort work properly
- Fix process time collection to /proc/<PID>/ files where the user has no access to read
- Fix segmentation fault that happens randomly when the program is closed (possibly to do with how Qt is setup and configured)

## Low Priority

- Add exception handling to the startup file creation/writing
- Add apt-get package names for requirements
- Make the program close upon ctrl+c or ctrl+d when ran from terminal
- Add something to the description column in the process list
- Fix the CPU usage showing 0 sometimes


## Resources

Read about RAM on Linux
http://www.linuxatemyram.com/

CPU usage
https://github.com/Leo-G/DevopsWiki/wiki/How-Linux-CPU-Usage-Time-and-Percentage-is-calculated

CPU usage and RAM usage calculations are based off htop's source code.
