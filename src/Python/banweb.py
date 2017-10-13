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
import audit
import os

################################################################################
# Classes
###

class Banweb(object):
    """Banweb
    Class representing the server at banweb.mtu.edu. Its class methods interface
    with the actual server to obtain information.

    Attributes:
        _ubase -- base URL
        _ulogin -- login page URL
        _uauditreq -- Audit Request page
        _jar -- cookie jar
        _session -- requests.Session object
    """

    def __init__(self):
        """
        __init__:
        Constructor for the Banweb class.

        Args:
        	None.

        Returns:
        	None.

        Raises:
        	None.
        """
        self._ubase = 'https://www.banweb.mtu.edu/'
        self._ulogin = 'pls/owa/twbkwbis.P_ValLogin'
        self._uauditreq = 'pls/owa/mtu_degree_audit.p_request_audit_complete'

        # Create cookie jar and http handler
        self._jar = cookiejar.CookieJar()


    def login(self, name, pass_):
        """
        login:
        Login to the Banweb server as a user

        Args:
        	name: The caller's Username
                pass_: The User's password

        Returns:
        	None.

        Raises:
        	RuntimeError: In the event that Banweb returns a status code
                    that is NOT 200.
        """
        self._session = requests.Session()
        # Once to fill the cookie jar
        ret = self._session.post(self._ubase + "" + self._ulogin,
                                 data={'sid':name, 'PIN':pass_})
        if ret.status_code != 200:
            raise RuntimeError('Post returned error code: ' + ret.status_code)

        # Once to log in.
        ret = self._session.post(self._ubase + "" + self._ulogin,
                                 data={'sid':name, 'PIN':pass_})
        if ret.status_code != 200:
            raise RuntimeError('Post returned error code: ' + ret.status_code)

    def getaudit(self): # TODO: add options for 'List All Requirements'
        """
        getaudit:
        Request a degree audit from the Banweb Server.

        Args:
        	None.

        Returns:
        	Audit obj: An Audit object initialized with the data retrieved.

        Raises:
        	RuntimeError: In the event that the server returns an error.
                RuntimeError: Error parsing the degree audit.
                OSError: In the event that a file operation is not supported.
        """
        print('Waiting on Banweb to run an audit...')
        ret = self._session.post(self._ubase + '' + self._uauditreq,
                                 data={'fdgrog': '', 'audit_switch': 'N'})
        if ret.status_code != 200:
            raise RuntimeError('Banweb server returned error code: '
                               + ret.status_code)

        root = etree.HTML(ret.text)
        degaudit = None
        for element in root.iter():
            if element.get('class') == 'pagebodydiv':
                for child in element.iter():
                    if child.tag == 'a' and \
                       re.search('darwinia', child.get('href')):
                        degaudit = child.get('href')
                        break

        if degaudit == None:
            raise RuntimeError('Error when parsing degree audit.')

        degaudit = self._session.get(degaudit)
        try:
            fh = open('degaudit.html', 'w')
            fh.write(degaudit.text)
            fh.close()
            degaudit = audit.Audit('degaudit.html')
            # os.unlink('degaudit.html') # TODO: Uncomment this.
            return degaudit
        except OSError as e:
            raise

################################################################################
# Main
###

if __name__ == '__main__':
    print('You\'re silly! This isn\'t a <em>real</em> module!')

################################################################################
