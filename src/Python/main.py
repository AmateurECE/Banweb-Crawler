#!/usr/bin/env python3
################################################################################
# NAME:		    main.py
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    This is the main execution file for the Banweb Crawler
#                   application. The flow of execution spreads outwards from
#                   this point.
#
# CREATED:	    08/08/2017
#
# LAST EDITED:	    11/03/2017
###

################################################################################
# Imports
###

import os
import audit
import banweb
from sys import platform

################################################################################
# Functions
###

def setecho(on):
    global out
    if platform == 'win32':
        if on == False:
            out = sys.stdout
            sys.stdout = open('Nul', 'w')
        else:
            sys.stdout.close()
            sys.stdout = out
    else:
        if on == False:
            os.system('stty -echo')
        else:
            os.system('stty echo')

def main():
    """
    main:
    Does the thing.

    Args:
    	None.

    Returns:
    	None.

    Raises:
    	
    """
    # TODO: The following code is for testing only.
    name = input("Username: ")
    setecho(False)
    passwd = input("Password: ")
    setecho(True)
    print()
    ######

    mybanweb = banweb.Banweb()
    mybanweb.login(name, passwd)
    audit = mybanweb.getaudit()
    
################################################################################
# Main
###

if __name__ == '__main__':
    main()

# EOF ##########################################################################
