/*******************************************************************************
 * NAME:	    confparse.c
 *
 * AUTHOR:	    Ethan D. Twardy
 *
 * DESCRIPTION:	    The source code for the API in confparse.h
 *
 * CREATED:	    08/05/2017
 *
 * LAST EDITED:	    08/05/2017
 ***/

/*******************************************************************************
 * INCLUDES
 ***/

#include <stdio.h>
#include <stdlib.h>
#include <pcre.h>

#include "confparse.h"
#include "stopif.h"

/*******************************************************************************
 * MACRO DEFINITIONS
 ***/

#define CP_ERRMSG "confparse(): There was an error parsing the file. " \
  "Returning to main()."

#define SET_N_RET(errval) {			\
    ret_err = errval;				\
    goto err_exit;				\
  }

/* Internal macros for variable parsing. */
/* Maybe this seems kind of superfluous? But it means I don't
 * have to remember the struc var names. */
#define REQ_COURSES(confstruc) ((confstruc)->req_courses)
#define ONLINE(confstruc) ((confstruc)->online)
#define DEGREE_REQ(confstruc) ((confstruc)->degree_req)
#define SCHEDULE(confstruc) ((confstruc)->schedule)

/*******************************************************************************
 * TYPE DEFINITIONS
 ***/

/* Internal struct definiton for use with static functions. */
typedef struct regstruc_t {

  char * input; /* Input string */
  size_t input_size; /* Size of input string. */
  char * regex; /* regex. */
  
  int matches; /* Number of matches */
  int ovec[30]; /* Number of matches (sizeof match array). 30 is standard */

  pcre * pcre; /* PCRE internal type. */

} regstruc_t;

/*******************************************************************************
 * STATIC FUNCTION PROTOTYPES
 ***/

static int match_string(regstruc_t * regstruc);

/*******************************************************************************
 * API FUNCTION PROTOTYPES
 ***/

/*******************************************************************************
 * FUNCTION:	    confparse
 *
 * DESCRIPTION:	    Parses a configuration file and returns a struct to the main
 *		    program.
 *
 * ARGUMENTS:	    conf: (FILE *) -- pointer to the config file.
 *
 * RETURN:	    conf_options * -- pointer to the conf_options struct.
 *
 * NOTES:	    none.
 ***/
conf_options * confparse(FILE * conf)
{
  /****
   * Check for errors
   */
  extern error_mode; /* Defined in stopif.h */
  char loc_err = error_mode;
  error_mode = ''; /* Save the value and unset. */
  int ret_err;

  conf_options * opts = malloc(sizeof(conf_options));

  Stopif(conf == NULL, {ret_err = ERR_NULL_FP; goto error_exit}, CP_ERRMSG);

  /****
   * Read the file
   */
  char buff[1024]; /* This should be enough. */
  while (!feof(conf)) {
    if (!fgets(buff, 1024, conf))
      SET_N_RET(ERR_READING);

    if (buff[0] == '#')
      continue; /* # is the comment tag. Don't parse these lines. */

    regstruc_t * regstruc;
    *regstruc = (regstruc_t){.input = buff,
			     .input_size = sizeof(buff),
			     .regex = " = "};
    if (match_string(regstruc)) {
      char * var_name = 
    }
  }

 error_exit: {
    error_mode = loc_error; /* Restore error_mode. */
    opts->err_mask = ret_err;
  }
}

/*******************************************************************************
 * STATIC FUNCTION DEFINITIONS
 ***/

/*******************************************************************************
 * FUNCTION:	    match_string
 *
 * DESCRIPTION:	    Matches the string 'regex' in the string 'input'
 *
 * ARGUMENTS:	    regstruc: (regstruc_t *) -- This is an internal type.
 *			Wrapping in a struct makes for easy extension.
 *
 * RETURN:	    int -- 1 if there is a match, 0 if not, -1 on failure.
 *
 * NOTES:	    none.
 ***/
static int match_string(regstruc_t * regstruc)
{

  /* Not a whole lot of error checking here. */
  if (regstruc == NULL)
    return -1;
  if (regstruc->input == NULL || regstruc->regex == NULL)
    return -1;

  char * iserror;
  int erroffset;
  
  regstruc->pcre = pcre_compile(regstruc->regex, 0, &iserror, &erroffset, NULL);
  if (regstruc->pcre == NULL)
    return -1;

  int rc = pcre_exec(regstruc->pcre,
		     NULL,
		     regstruc->input,
		     regstruc->input_size,
		     0,
		     0,
		     regstruc->ovec,
		     30);

  int ret_code;
  if (rc == PCRE_ERROR_NOMATCH) ret_code = 0;
  else if (rc < 0 && rc != PCRE_ERROR_NOMATCH) ret_code = -1;
  else ret_code = 1;
  
  pcre_free(regstruc->pcre);
  if (rc > 0) regstruc->matches = rc;
  return ret_code;
}

/******************************************************************************/
