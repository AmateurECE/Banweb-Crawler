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
# LAST EDITED:	    08/08/2017
###

################################################################################
# Imports
###

import os

################################################################################
# Functions
###

def main():
    """The main method - the top of the stack."""
    # TODO: The following code is for testing only.
    name = raw_input("Username: ")
    os.system("stty -echo") # Turn off echo for the password
    passwd = raw_input("Password: ")
    os.system("stty -echo") # Turn it back on.
    ### END TODO ###

################################################################################
# Main
###

if __name__ == '__main__'::
    main()

# EOF ##########################################################################
