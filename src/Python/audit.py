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
    def __init__(self, auditfn):
        """
        __init__:
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
            # TODO: Get all <span> tags that match 'auditLineType_...'
            #   (Create explicit list of possible tags.)
            fh.close()
        except OSError as e:
            raise        

################################################################################
# Main
###

if __name__ == '__main__':
    print('You\'re silly! This isn\'t a <em>real</em> module!')

################################################################################
