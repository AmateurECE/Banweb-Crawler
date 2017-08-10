#!/usr/bin/env python3
################################################################################
# NAME:		    banweb.py
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    This module provides an interface to the Banweb server, and
#                   is used by main to perform some basic operations, such as
#                   navigating the website and logging in.
#
# CREATED:	    08/09/2017
#
# LAST EDITED:	    08/09/2017
###

################################################################################
# Imports
###

import http.cookiejar as cookiejar
import requests

################################################################################
# Classes
###

class Banweb(object):
    """Interfaces with the Banweb Server to get web pages, etc:
    Datum:
        _ulogin -- login page URL
        _jar -- cookie jar
        _session -- reqeusts.Session object
    """

    def __init__(self):
        """Initializes a Banweb Object"""
        self._ulogin = "https://www.banweb.mtu.edu/pls/owa/twbkwbis.P_ValLogin"

        # Create cookie jar and http handler
        self._jar = cookiejar.CookieJar()


    def login(self, name, pass_):
        """Login to the Banweb server as a user"""
        self._session = requests.Session()
        # Once to fill the cookie jar
        ret = self._session.post(self._ulogin, data={'sid':name, 'PIN':pass_})
        # Once to log in.
        ret = self._session.post(self._ulogin, data={'sid':name, 'PIN':pass_})

################################################################################
# Main
###

if __name__ == '__main__':
    print("hey, what's up?")

################################################################################
