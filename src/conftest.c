/*******************************************************************************
 * NAME:	    conftest.c
 *
 * AUTHOR:	    Ethan D. Twardy
 *
 * DESCRIPTION:	    Test script to ensure that the program correctly parses
 *		    configuration files.
 *
 * CREATED:	    08/07/2017
 *
 * LAST EDITED:	    08/07/2017
 ***/

/*******************************************************************************
 * INCLUDES
 ***/

#include "confparse.h"

/*******************************************************************************
 * MAIN
 ***/

int main(int argc, char * argv[])
{

  char * filename = "test.conf";

  conf_options * options = confparse(filename);

  // TODO: print out the struct returned.
  
}

/******************************************************************************/
