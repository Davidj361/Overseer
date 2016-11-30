# Comp300Group5
## A task manager GUI application for Linux
### Created by: Trent McNabb & David Jatczak

# TODO LIST
- Make Proc.getTotalMem() more efficient
- Choose a polling rate and make Proc read its data for that interval, consider threading or see if the Proc class is on a separate thread
- Fix decimal places for ram precentage
- Have username actually translated to the proper username
- Implement sending signal via a right-click context menu on a process
- Hook onto Qt's update/refresh method so that it grabs values from our Proc class
- Have Qt columns be able to sort, get rid delete right-click option in process list

## Resources

Read about RAM on Linux
http://www.linuxatemyram.com/

CPU usage
https://github.com/Leo-G/DevopsWiki/wiki/How-Linux-CPU-Usage-Time-and-Percentage-is-calculated
