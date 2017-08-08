################################################################################
# NAME:		    conftest.sh
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    Compiles conftest for testing.
#
# CREATED:	    08/07/2017
#
# LAST EDITED:	    08/07/2017
###

gcc -g -Wall -O0 `pkg-config --libs --cflags libpcre` \
    -o conftest conftest.c confparse.c

if [[ $? != "0" ]]; then
    exit
fi

./conftest
rm -rf conftest
