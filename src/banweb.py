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
from lxml import etree
import re

################################################################################
# Classes
###

class Banweb(object):
    """Interfaces with the Banweb Server to get web pages, etc:
    Datum:
        _ubase -- base URL
        _ulogin -- login page URL
        _uauditreq -- Audit Request page
        _jar -- cookie jar
        _session -- reqeusts.Session object
    """

    def __init__(self):
        """Initializes a Banweb Object"""
        self._ubase = 'https://www.banweb.mtu.edu/'
        self._ulogin = 'pls/owa/twbkwbis.P_ValLogin'
        self._uauditreq = 'pls/owa/mtu_degree_audit.p_request_audit_complete'

        # Create cookie jar and http handler
        self._jar = cookiejar.CookieJar()


    def login(self, name, pass_):
        """Login to the Banweb server as a user"""
        self._session = requests.Session()
        # Once to fill the cookie jar
        ret = self._session.post(self._ubase + "" + self._ulogin,
                                 data={'sid':name, 'PIN':pass_})
        # Once to log in.
        ret = self._session.post(self._ubase + "" + self._ulogin,
                                 data={'sid':name, 'PIN':pass_})

    def get_audit(self): # Eventually add options for 'List All Requirements'
        """Request a degree audit from the Banweb Server."""
        print('Waiting on Banweb to run an audit...')
        ret = self._session.post(self._ubase + "" + self._uauditreq,
                                 data={'fdgrog': '', 'audit_switch': 'N'})
        root = etree.HTML(ret.text)
        for element in root.iter():
            if element.get('class') == 'pagebodydiv':
                for child in element.iter():
                    if child.tag == 'a' and \
                       re.search('darwinia', child.get('href')):
                        audit = child.get('href')
                        break

        if audit == None:
            # TODO: Throw an exception here.
            return

        audit = self._session.get(audit)
        fh = open("degaudit.html", 'w')
        fh.write(audit.text)
        fh.close()
        return True

################################################################################
# Main
###

if __name__ == '__main__':
    print("hey, what's up?")

################################################################################
