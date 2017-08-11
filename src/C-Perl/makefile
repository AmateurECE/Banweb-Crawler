################################################################################
# NAME:		    makefile
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    Makefile for the Banweb Crawler
#
# CREATED:	    08/05/2017
#
# LAST EDITED:	    08/05/2017
###

CFLAGS = -g -Wall -O0 \
	-I/usr/include/libxml2 \
	-I/usr/local/Cellar/pcre/8.39/include
LDLIBS = -lcurl -lxml2 -L/usr/local/Cellar/pcre/8.39/lib -lpcre
CC=gcc
OBJS = 

crawler: $(OBJS)
