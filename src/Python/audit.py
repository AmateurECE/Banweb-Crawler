#!/usr/bin/env python3
################################################################################
# NAME:		    audit.py
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    This module provides a class interface for the Audit class.
#                   This class contains information about the student's degree
#                   audit, and writes and reads this information from an XML
#                   document.
#
# CREATED:	    08/09/2017
#
# LAST EDITED:	    08/09/2017
###

################################################################################
# Imports
###

from lxml import etree
import os
import json

################################################################################
# Classes
###

class Audit(object):
    """Audit
    The class representing a degree audit in data-structure form.

    Attributes:
    	_htmlfn: The name of the Audit's HTML file
        _jsonfn: The name of the Audit's JSON file
        _data: Array of dicts representing all of the useful information.
    """

    def __init__(self, auditfn):
        """__init__:
        Initialize an Audit object.

        Args:
        	auditfn: Name of a file containing the raw HTML of the audit.

        Returns:
        	None.

        Raises:
        	OSError: In the event that a file operation is not supported.
        """
        try:
            self._htmlfn = auditfn
            fh = open(auditfn, 'r')
            root = etree.HTML(fh.read())
            self._data = self.parsehtml(root)
            fh.close()
        except OSError as e:
            raise        

    def parsehtml(self, root):
        """parsehtml:
        Parses the HTML file that we got from the banweb server.

        Args:
        	root: The root node of the HTML file, <html>

        Returns:
        	array of dicts representing the useful data.

        Raises:
        	TypeError: If root is not an instance of etree.Element, or None.
        """
        if root == None or not isinstance(root, etree._Element):
            raise TypeError('parsehtml takes an etree.Element argument.')

        data = list()
        for tag in root.iter('font'):
            # TODO: Get only the ones we care about
            data.append(self.parsefont(tag))
        return data

    def parsefont(self, font):
        """parsefont:
        This function parses a font tag and returns a dict.

        Args:
        	font: The font tag.

        Returns:
        	dict: containing useful data

        Raises:
        	None.
        """
        if font.tag != 'font':
            raise ValueError('Argument to parsefont must be a <font> tag.')

        data = dict()
        num = 0
        for span in font.iter('span'):
            data['--'.join(((span.get('class') if span.get('class') != None
                             else "nil", str(num))))] = dict(span.attrib)
            # TODO: Extract info with a hugh mungus and poorly formed if-elif stmt
            num += 1

        return data

################################################################################
# Main
###

if __name__ == '__main__':
    myaudit = Audit('degaudit.html')
    try:
        outfh = open('temp.json', 'w')
        json.dump(myaudit._data, outfh)
        outfh.close()

        unique = list()
        for one in myaudit._data:
            for key in one.keys():
                if 'class' in one[key]:
                    if not one[key]['class'] in unique:
                        unique.append(one[key]['class'])
        unique.sort()
        print('\n'.join(unique))
    except OSError as e:
        raise
    print('Done!')

################################################################################
