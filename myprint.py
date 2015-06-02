"""
File for printing INFO to screen.
To turn off print, set change flag.
"""

def myprint(output, flag):
    if flag == "info":
        print "[" + flag.upper() +"] " + output + "\n"
