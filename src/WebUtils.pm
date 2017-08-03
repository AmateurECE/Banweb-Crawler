################################################################################
# NAME:		    refresh
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    In the case that banweb gives us a bogus gateway page,
#		    load the actual one.
#
# CREATED:	    08/03/2017
#
# LAST EDITED:	    08/03/2017
###

################################################################################
# Inclusions
###

use strict;
use warnings;

package WebUtils;

sub WebUtils::formparse {

    if (m/--- FORM/) {
	m/"(.*)"/;
	print "s $1";	# 's' indicates to the parent process that this is the
			# script to post to.
    } elsif (m/NAME="(.*)"/) {
	print "n $1"; # 'n' indicates to the parent process that this is the
			# name of a field to input.
    }
    
}

################################################################################
