# LOG: BEGINNING -------------------------------------------------------------#
# This is where we imlement the logs.
from enum import Enum


# The log recorder
class Log(dict):
    '''
        The log, dictionary-shaped. For now, only the values are used. 
        So you can see it as a list of warnings.
    '''
    def add(self, logclass, *args):
        '''
            Inserts a new message, identified with an enum value.
            Such message (a string) is completed with the *args, 
            input(s): the enum, the arguments *args (optional)
        '''
        # The log class name is turned intp a more human-readable way:
        key = logclass.name.replace('_', ' ').lower()
        
        if key in self:
            pass
        else:
            self[key] = []
        #
        self[key].append(logclass.value%args)
        #
    #
#

# The standard warning messages.
class LOG(Enum):
    
    # documentclass warnings.
    NO_DOCUMENTCLASS    = 'WARNING: documentclass: Nothing about documentclass in the preferences file: You should harcode your \documentclass markup.'
    OPTION              = 'WARNING: documentclass: The value %s of %s in nonstandard. If you deal with the standard package, then it is a mistyping.'
    NO_OPTION           = 'WARNING: documentclass: %s is not a standard option. If you deal with the standard package, then it is a mistyping.'
    NO_OPTION_          = 'WARNING: documentclass: No [option] for class %s.'
    NO_STANDARD_CLASS   = 'WARNING: documentclass: %s is not a standard class. If you deal with the standard package, then it is a mistyping.'
    
    # Custom page warning.
    CUSTOM              = 'Warning: %s: %s: Not implemented.'
    
    # Language settings warning.
    LANGUAGE            = 'WARNING: You did not set any language preference. '
#
# LOG: END -------------------------------------------------------------------#