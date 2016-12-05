# Comp300Group5
## A task manager GUI application for Linux
### Created by: Trent McNabb & David Jatczak

# Requirements:
- Ubuntu 16.04 (Tested on)
- python3
- PyQt5
- xlib for python3, package: python3-xlib

# To Run:
Go into the main directory of the repo, type into terminal: python3 overseer.py

# TODO LIST
- Make Proc.getTotalMem() more efficient
- Choose a polling rate and make Proc read its data for that interval, consider threading or see if the Proc class is on a separate thread
- Fix decimal places for ram precentage
- Have username actually translated to the proper username
- Implement sending signal via a right-click context menu on a process
- Give the program an option to launch on OS's startup
- Have ctrl-alt-del bring up a dialog to ask if you want to see task manager
- Have ctrl+shift+esc work as shortcut to bring up task manager
- Fix segmentation fault that happens randomly (possibly to do with the startup file creation)
- Give the program an icon
- Make the program close upon ctrl+c or ctrl+d
- Add exception handling to the startup file creation/writing
- Add apt-get package names for requirements

## Resources

Read about RAM on Linux
http://www.linuxatemyram.com/

CPU usage
https://github.com/Leo-G/DevopsWiki/wiki/How-Linux-CPU-Usage-Time-and-Percentage-is-calculated
