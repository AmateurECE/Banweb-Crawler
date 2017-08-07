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
#include <string.h>

#include "confparse.h"
#include "stopif.h"

/*******************************************************************************
 * MACRO DEFINITIONS
 ***/

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
  pcre_extra * extra; /* PCRE internal type. */

} regstruc_t;

/*******************************************************************************
 * STATIC FUNCTION PROTOTYPES
 ***/

static int regstruc_init(regstruc_t * regstruc, char * regex);
static int regstruc_match_string(regstruc_t * regstruc);
static int regstruc_destroy(regstruc_t * regstruc);

static int conf_populate(conf_options * opts, char * varname, char * varval);

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

  Stopif(conf == NULL, SET_N_RET(ERR_NULL_FP));

  regstruc_t * regstruc;
  if (!regstruc_init(regstruc, "(.*) ?= ?(.*)"))
    SET_N_RET(ERR_PARSING);

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
			     .input_size = sizeof(buff)};
    if (match_string(regstruc)) {
      /* ovec[2] - ovec[3]: Start and end of capture group 1, respectively.
       * ovec[4] - ovec[5]: Start and end of capture group 2, respectively.
       */
      char * varname = strndup(regstruc->input + regstruc->ovec[2],
			       regstruc->ovec[3] - regstruc->ovec[2]);
      char * varval = strndup(regstruc->input + regstruc->ovec[4],
			      regstruc->ovec[5] - regstruc->ovec[4]);

      int pop_ret = conf_populate(opts, varname, varval);
      if (pop_ret == -1) {
	fprintf(stderr, "Unrecognized option \"%s\"", varname);
      } else if (pop_ret == -2) {
	fprintf(stderr, "The value \"%s\" for option \"%s\" is not valid.",
		varval, varname);
      }

      free(varname);
      free(varval);
      /* Assume that insertion was successful. */
      
    }
  }

  regstruc_destroy(regstruc);
  return opts;

 error_exit: {
    error_mode = loc_error; /* Restore error_mode. */
    opts->err_mask = ret_err;
    return NULL;
  }
}

/*******************************************************************************
 * FUNCTION:	    conf_options_destroy
 *
 * DESCRIPTION:	    Frees memory associated with a conf_options pointer.
 *
 * ARGUMENTS:	    opts: (conf_options *) -- the pointer to the struct.
 *
 * RETURN:	    void.
 *
 * NOTES:	    none.
 ***/
void conf_options_destroy(conf_options * conf)
{

  for (int i = 0; i < REQ_COURSES(conf)_size; i++)
    free(REQ_COURSES(conf)[i]);

  for (int i = 0; i < DEG_REQUIREMENTS(conf)_size; i++)
    free(DEG_REQUIREMENTS(conf)[i]);

  free(conf);

}

/*******************************************************************************
 * STATIC FUNCTION DEFINITIONS
 ***/

/*******************************************************************************
 * FUNCTION:	    regstruc_init
 *
 * DESCRIPTION:	    Initializes a regstruc object.
 *
 * ARGUMENTS:	    regstruc: (regstruc_t *) -- the regstruct object to init.
 *		    regex: (char *) -- initializes with this regex.
 *
 * RETURN:	    int -- 0 on success, -1 otherwise.
 *
 * NOTES:	    none.
 ***/
static int regstruc_init(regstruc_t * regstruc, char * regex)
{

  if (asprintf(&regstruc->regex, "%s", regex) < 0)
    return -1;
  
  char * iserror = NULL;
  int erroffset = 0;
  
  regstruc->pcre = pcre_compile(regstruc->regex, 0, &iserror, &erroffset, NULL);
  if (regstruc->pcre == NULL || iserror != NULL)
    return -1;

  regstruc->extra = pcre_study(regstruc->pcre, 0, &iserror);
  if (iserror != NULL)
    return -1;

  return 0;
}

/*******************************************************************************
 * FUNCTION:	    regstruc_match_string
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
static int regstruc_match_string(regstruc_t * regstruc)
{

  /* Not a whole lot of error checking here. */
  if (regstruc == NULL)
    return -1;
  if (regstruc->input == NULL || regstruc->regex == NULL)
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
  
  if (rc > 0) regstruc->matches = rc;
  return ret_code;
}

/*******************************************************************************
 * FUNCTION:	    regstruc_destroy
 *
 * DESCRIPTION:	    Frees memory allocated with a regstruc.
 *
 * ARGUMENTS:	    regstruc: (regstruc_t *) -- pointer to the object.
 *
 * RETURN:	    void.
 *
 * NOTES:	    none.
 ***/
static void regstruc_destroy(regstruc_t * regstruc)
{

  pcre_free(regstruc->pcre);
  if (regstruc->exra != NULL)
    pcre_free_study(regstruc->extra);
  free(regstruc->regex);
  
}

/*******************************************************************************
 * FUNCTION:	    conf_populate
 *
 * DESCRIPTION:	    Populate the conf_options struct with values provided.
 *
 * ARGUMENTS:	    opts: (conf_options *) -- the struct to populate
 *		    varname: (char *) -- the name of the variable.
 *		    varval: (char *) -- the value of the variable.
 *
 * RETURN:	    int -- 0 on success, -1/-2 if the option is not recognized.
 *
 * NOTES:	    A return of -1 indicates that the option is not recognized,
 *		    A return of -2 indicates the value specified is not valid
 *		    for the option specified.
 ***/
static int conf_populate(conf_options * opts, char * varname, char * varval)
{
  // TODO HERE: Complete this if-else-if block.
  if (!strcmp(varname, "REQ_COURSES")) {

    if (REQ_COURSES(opts) == NULL)
      fprintf(stderr, "REQ_COURSES is already defined.");

    int arr_size = 0;
    while (strtok(varval, ",")) arr_size++;

    REQ_COURSES(opts) = malloc(arr_size * sizeof(course_t));
    REQ_COURSES(opts)_size = arr_size;

    int i = 0;
    char * entry = NULL;
    while ((entry = strtok(varval), ",") != NULL) {
      REQ_COURSES(opts)[i]->department = strndup(entry, 2);
      REQ_COURSES(opts)[i]->number = strtol(entry + 2, NULL, 10);
      i++;
    }

  } else if (!strcmp(varname, "ONLINE")) {

    if (!strcmp(varval, "NONE"))
      ONLINE(opts) = NONE;
    else if (!strcmp(varval, "SOME"))
      ONLINE(opts) = SOME;
    else if (!strcmp(varval, "ALL"))
      ONLINE(opts) = ALL;
    else return -2;
    
  } else if (!strcmp(varname, "DEGREE_REQ")) {

    int arr_size = 0;
    while (strtok(varval, ",")) arr_size++;

    DEGREE_REQ(opts) = malloc(arr_size * sizeof(char *));
    DEGREE_REQ(opts)_size = arr_size;

    int i = 0;
    char * entry = NULL;
    while ((entry = strtok(varval, ",")) != NULL)
      DEGREE_REQ(opts)[i] = strdup(entry);

  } else if (!strcmp(varname, "SCHEDULE")) {
    return -1;
  } else {
    return -1;
  }

  return 0;
}

/******************************************************************************/
