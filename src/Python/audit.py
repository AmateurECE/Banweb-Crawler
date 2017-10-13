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
            fh = open(auditfn, 'r')
            root = etree.HTML(fh.read())
            _data = parsehtml(root)
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
        if root == None or not root.iselement()
            raise TypeError('parsehtml takes an etree.Element argument.')

        data = list()
        for tag in root.iter('font'):
            # TODO: Get only the ones we care about
            data.append(parsefont(tag))

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

        # TODO: Extract info with a humongous and poorly formed if-elif stmt.

################################################################################
# Main
###

if __name__ == '__main__':
    print('You\'re silly! This isn\'t a <em>real</em> module!')

################################################################################
