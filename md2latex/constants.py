# Constants

# Logic: BEGINNING -----------------------------------------------------------#
# Element of TRUE means True
TRUE  = (
    True,  'true', 'True', 
    'yes', 'Yes',  'YES', 'Y', 
    'on',  'On',   'ON'
)
# Element of FALSE means False
FALSE = (
    None, '', 
    False, 'false', 'False', 
    'no',  'No',    'NO',   'N', 
    'off', 'Off',   'OFF'
)

# Synonyms
NO    = FALSE
YES   = TRUE
BOOLEAN = frozenset(YES+NO)
# Logic: END -----------------------------------------------------------------#

# Markdown extensions: BEGINNING ---------------------------------------------#
# For file input: 
# \input{${myfile}}} will be converter to the LaTeX markup 
# \input{${myfile}}}
SUBSTRING_OPENING = '\inputmd{'
SUBSTRING_CLOSING = '}'
# Markdown extensions: END ---------------------------------------------------#

# Implementation: BEGINNING --------------------------------------------------#
PATH_DEFAULT_ = frozenset(('default', 'default path'))
# Implementation: END --------------------------------------------------------#
