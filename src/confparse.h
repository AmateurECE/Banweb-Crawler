/*******************************************************************************
 * NAME:	    confparse.h
 *
 * AUTHOR:	    Ethan D. Twardy
 *
 * DESCRIPTION:	    Public interface for the configuration file parser.
 *
 * CREATED:	    08/05/2017
 *
 * LAST EDITED:	    08/05/2017
 ***/

#ifndef __ET_CONFPARSE_H__
#define __ET_CONFPARSE_H__

/*******************************************************************************
 * INCLUDES
 ***/

#include <stdlib.h>
#include <stdbool.h>

/*******************************************************************************
 * MACRO DEFINITIONS
 ***/

/* Parsing errors. */
#define ERR_PARSING 0x00000001 /* Standard parse error, nonspecific. */
#define ERR_NULL_FP 0x00000002 /* Passed a null pointer. */
#define ERR_READING 0x00000003 /* Error when reading. */

/*******************************************************************************
 * TYPE DEFINITIONS
 ***/

typedef enum option {NONE, SOME, ALL};

typedef struct conf_options {

int * req_courses;	/* Courses that are required to be returned. */
option online;		/* Return online courses? */
int * degree_req;	/* Degree requirements that are to be filled. */
bool shecule;		/* Create a schedule? */
int err_mask;		/* Non-zero if there was an error. */

} conf_options;

/*******************************************************************************
 * API FUNCTION PROTOTYPES
 ***/

extern conf_options * confparse(FILE * conf);

#endif /* __ET_CONFPARSE_H__ */

/******************************************************************************/
