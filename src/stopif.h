/*******************************************************************************
 * NAME:	    stopif.h
 *
 * AUTHOR:	    Ethan D. Twardy
 *
 * DESCRIPTION:	    Stopif macro. Performs a stop operation when the bool
 *		    provided evaluates to false. This 
 *
 * CREATED:	    08/05/2017
 *
 * LAST EDITED:	    08/05/2017
 ***/

#ifndef __ET_STOPIF_H__
#define __ET_STOPIF_H__

/*******************************************************************************
 * INCLUDES
 ***/

#include <stdio.h>
#include <stdlib.h> //abort

/*******************************************************************************
 * MACRO DEFINITIONS
 ***/

#define Stopif(assertion, error_action, ...) {                    \
        if (assertion){                                           \
            fprintf(error_log ? error_log : stderr, __VA_ARGS__); \
            fprintf(error_log ? error_log : stderr, "\n");        \
            if (error_mode=='s') abort();                         \
            else                 {error_action;}                  \
        } }

/*******************************************************************************
 * GLOBAL VARIABLES
 ***/

char error_mode;
FILE *error_log;

#endif /* __ET_STOPIF_H__ */

/******************************************************************************/
