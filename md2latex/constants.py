# Constants

# Logic: BEGINNING -----------------------------------------------------------#
# Element of TRUE means True
TRUE  = (
    1, 
    True,  'true', 'True', 
    'on',  'On',   'ON',
    'yes', 'Yes',  'YES', 'Y', 
)
# Element of FALSE means False
FALSE = (
    0, 
    None, '', 
    False, 'false', 'False', 
    'off', 'Off',   'OFF',
    'no',  'No',    'NO',   'N', 
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

# Inserting a code as comment:
# The following string embedds all relevant options
# @see package 'listings' on CTAN.org
# TOODO: No constant string
COMMENTCODESTARTS = \
    '\lstset{tabsize = 4, \
    showstringspaces = false, \
    commentstyle = \color{gray}, \
    keywordstyle = \color{purple}, \
    stringstyle = \color{red}, \
    rulecolor = \color{black}, \
    basicstyle = \small \\fw, \
    breaklines = true, \
    numberstyle = \\tiny,}{\color{blue} \
    \\begin{lstlisting}[language = TeX, \
    frame = trBL , firstnumber = last]'
COMMENTCODEENDS='\end{lstlisting}}'
# Markdown extensions: END ---------------------------------------------------#

# Implementation: BEGINNING --------------------------------------------------#
PATH_DEFAULT_ = frozenset(('default', 'default path'))
# Implementation: END --------------------------------------------------------#
