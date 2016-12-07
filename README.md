# Comp300Group5
### A task manager GUI application for Linux
### Created by: Trent McNabb & David Jatczak

# Requirements:
- Ubuntu 16.04 (Tested on)
- Python 3.5.2
- PyQt5

# To Run:
Clone or download the repository. Rename and move the repository folder as however you like.

Go into the main directory of the repository, type into terminal: python3 overseer.py

It should create a bash script as ~/openOverseer.sh, and you should get your logout shortcut disabled while 2 shortcuts are made in Ubuntu.

If you want to move the repository folder, just delete ~/openOverseer and the Overseer shortcuts and rerun overseer.py.

Note: Ctrl+Shift+Escape doesn't seem to work because shortcuts in Ubuntu with Escape just don't work.

# TODO LIST

## High Priority

- Implement ending processes in the process's tab
- Finish CPU usage calculation (it calculates since boot time)
- Go through all the code and fix the FIXME comments
- Have username actually translated to the proper username

## Medium Priority

- Give the program an icon
- Finish applications tab
- Give the program an option to launch on OS's startup (to read for shortcuts)
- Fix segmentation fault that happens randomly (possibly to do with the startup file creation or how Qt is setup)

## Low Priority

- Add exception handling to the startup file creation/writing
- Add apt-get package names for requirements
- Make Proc.getTotalMem() more efficient
- Make the program close upon ctrl+c or ctrl+d when ran from terminal


## Resources

Read about RAM on Linux
http://www.linuxatemyram.com/

CPU usage
https://github.com/Leo-G/DevopsWiki/wiki/How-Linux-CPU-Usage-Time-and-Percentage-is-calculated

CPU usage and RAM usage calculations are based off htop's source code.
