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
import re

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

    def __init__(self, auditfn, logfile=None):
        """__init__:
        Initialize an Audit object.

        Args:
        	auditfn: Name of a file containing the raw HTML of the audit.
                logfile: Filehandle to log warnings, etc. to.

        Returns:
        	None.

        Raises:
        	OSError: In the event that a file operation is not supported.
        """
        try:
            self._htmlfn = auditfn
            self._logfile = logfile
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

        req = {
            'header': None,
            'satisfied': None,
            'complete': None,
            'incomplete': None
        }
        # num = 0
        for span in font.iter('span'):
            # data['--'.join(((span.get('class') if span.get('class') != None
            #                  else "nil", str(num))))] = dict(span.attrib)
            # num += 1
            # TODO: Extract info with a hugh mungus and poorly formed if-elif st
            cls = span.get('class')
            if cls == "auditLineType_07_hText":
                # TODO: Decide if we need this.
                pass
            elif cls == "auditLineType_09_blankLine":
                # Not important
                pass
            elif cls == "auditLineType_10_okRequirementTitle":
                if req['header'] == None:
                    req['header'] = ''
                req['header'] += span.text if span.text else ''
                req['satisfied'] = True
            elif cls == "auditLineType_11_noRequirementTitle":
                if req['header'] == None:
                    req['header'] = ''
                req['header'] += span.text if span.text else ''
                req['satisfied'] = False
            elif cls == "auditLineType_12_okRequirementEarnedLine":
                # Do nothing. # TODO: Check for GPA here?
                # TODO: Setup logging
                pass
            elif cls == "auditLineType_13_noRequirementEarnedLine":
                # Do nothing. # TODO: Check for GPA here?
                pass
            elif cls == "auditLineType_15_noRequirementNeedsLine":
                # Do nothing. # TODO: Check for GPA here?
                pass
            elif cls == "auditLineType_16_okSubrequirementTLine":
                if req['complete'] == None:
                    req['complete'] = list()
                # TODO: Multiline titles?
                req['complete'].append({
                    'subreq-name': span.text,
                    'credits-complete': None,
                    'credits-in-progress': None,
                    'credits-incomplete': 0.0,
                    'courses': None,
                    'accept': None,
                    'reject': None,
                    'exceptions': None
                })
            elif cls == "auditLineType_17_noSubrequirementTLine":
                if req['complete'] == None:
                    req['complete'] = list()
                # TODO: Multiline titles?
                req['complete'].append({
                    'subreq-name': span.text,
                    'credits-complete': None,
                    'credits-in-progress': None,
                    'credits-incomplete': None,
                    'courses': None,
                    'accept': None,
                    'reject': None,
                    'exceptions': None
                })
            elif cls == "auditLineType_20_okSubrequirementEarnedLine":
                if req['complete'] == None or len(req['complete']) == 0:
                    self.log_error(((
                        'cond: auditLineType_20_okSubrequirementEarnedLine\n'
                        '\t\'complete\' member was not initialized correctly.'
                    )))
                    continue

                if re.match(r'IN-P --->\s*\d+\.\d+ credits', span.text):
                    req['complete'][-1]['credits-in-progress'] = (
                        re.match(r'IN-P --->\s*(\d+\.\d+) credits',
                                 span.text).group(1))
                else:
                    if re.match('\s*\d+\.\d+ credits added', span.text):
                        req['complete'][-1]['credits-complete'] = (
                            re.match(r'\s*(\d+\.\d+) credits added',
                                     span.text).group(1))
                    else:
                        self.log_error(format('%s%s%s' % (
                            'cond: auditLineType_20_okSubrequirementEarnedLine',
                            '\n\tNo valid regex to match string: ',
                            span.text
                        )))
                        pass
            elif cls == "auditLineType_21_noSubrequirementEarnedLine":
                if req['incomplete'] == None or len(req['incomplete']) == 0:
                    self.log_error(((
                        'cond: auditLineType_21_noSubrequirementEarnedLine\n'
                        '\t\'incomplete\' member was not initialized correctly.'
                    )))
                    continue

                if re.match(r'IN-P --->\s*\d+\.\d+ credits', span.text):
                    req['incomplete'][-1]['credits-in-progress'] = (
                        re.match(r'IN-P --->\s*(\d+\.\d+) credits',
                                 span.text).group(1))
                else:
                    if re.match('\s*\d+\.\d+ credits added', span.text):
                        req['incomplete'][-1]['credits-complete'] = (
                            re.match(r'\s*(\d+\.\d+) credits added',
                                     span.text).group(1))
                    else:
                        self.log_error(format('%s%s%s' % (
                            'cond: auditLineType_21_noSubrequirementEarnedLine',
                            '\n\tNo valid regex to match string: ',
                            span.text
                        )))
                        pass
            elif cls == "auditLineType_22_okSubrequirementCourses":
                if req['complete'] == None or len(req['complete']) == 0:
                    self.log_error(((
                        'cond: auditLineType_22_okSubrequirementCourses\n\t'
                        '\'complete\' member was not initialized correctly.'
                    )))
                    continue

                r = (r'((?:Fa|Sp|Su)\d{2}) '
                     r'(\w+)\s*(\d{4})\s*(\d\.\d+) (\w+) (.*)$')
                m = re.match(r''.join(((r'\s*', r))), span.text)
                if m:
                    if req['complete'][-1]['courses'] == None:
                        req['complete'][-1]['courses'] = list()
                    req['complete'][-1]['courses'].append({
                        'department': m.group(2),
                        'course': m.group(3),
                        'credits': m.group(4),
                        'grade': m.group(5),
                        'name': m.group(6),
                        'semester': m.group(1)
                    })
                else:
                    self.log_error(format('%s%s%s' % (
                        'cond: auditLineType_22_okSubrequirementCourses\n\t',
                        '\n\tNo valid regex to match string: ',
                        span.text
                    )))
                    pass
            elif cls == "auditLineType_23_noSubrequirementCourses":
                if req['incomplete'] == None or len(req['incomplete']) == 0:
                    self.log_error(((
                        'cond: auditLineType_23_noSubrequirementCourses\n\t'
                        '\'incomplete\' member was not initialized correctly.'
                    )))
                    continue

                r = (r'((?:Fa|Sp|Su)\d{2}) '
                     r'(\w+)\s*(\d{4})\s*(\d\.\d+) (\w+) (.*)$')
                m = re.match(r''.join(((r'\s*', r))), span.text)
                if m:
                    if req['incomplete'][-1]['courses'] == None:
                        req['incomplete'][-1]['courses'] = list()
                    req['incomplete'][-1]['courses'].append({
                        'department': m.group(2),
                        'course': m.group(3),
                        'credits': m.group(4),
                        'grade': m.group(5),
                        'name': m.group(6),
                        'semester': m.group(1)
                    })
                else:
                    self.log_error(format('%s%s%s' % (
                        'cond: auditLineType_23_noSubrequirementCourses\n\t',
                        '\n\tNo valid regex to match string: ',
                        span.text
                    )))
                    pass
            elif cls == "auditLineType_24_noRequirementNeedsSummaryLine":
                # TODO:
                pass
            elif cls == "auditLineType_25_noSubrequirementRejectCourses":
                # TODO:
                pass
            elif cls == "auditLineType_27_noSubrequirementRejectCourses":
                # TODO:
                pass
            elif cls == "auditLineType_28_okSubrequirementAcceptCourses":
                # TODO:
                pass
            elif cls == "auditLineType_29_noSubrequirementAcceptCourses":
                # TODO:
                pass
            elif cls == "null":
                # TODO:
                pass
            else:
                self.log_error(format('%s%s%s' % (
                    'Warning: No condition to match <span class="',
                    cls, '">'
                )))
                pass

        return req

    def log_error(self, msg):
        """log_error:
        If we were given a file to log to, log an error. Otherwise, do nothing.

        Args:
        	msg: The message

        Returns:
        	None.

        Raises:
        	None.
        """
        if self._logfile:
            self._logfile.write(msg)
            self._logfile.write('\n')

################################################################################
# Main
###

if __name__ == '__main__':
    try:
        logfh = open('log.txt', 'w')
        myaudit = Audit('degaudit.html', logfile=logfh)
        outfh = open('temp.json', 'w')
        json.dump(myaudit._data, outfh, indent=4)
        outfh.close()
        logfh.close()

        # unique = list()
        # for one in myaudit._data:
        #     for key in one.keys():
        #         if 'class' in one[key]:
        #             if not one[key]['class'] in unique:
        #                 unique.append(one[key]['class'])
        # unique.sort()
        # print('\n'.join(unique))
    except OSError as e:
        raise
    print('Done!')

################################################################################
