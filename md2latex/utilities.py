# Useful routines.. 

# It's all about returning strings!
def plural(array):
    '''
       If array contains more than one element, then a 's' is returned, 
       If not, then the empty string is returned.
    '''
    
    return '' + 's'*(len(array) > 1)
#

def cat(space, *array):
    '''
        Concatenates lines  (a ${space} is inserted between them).
    '''
    
    return space.join(array)
#

def lines(*array):
    '''
        "Stringifies' an array of strings: One string (only) per line.
    '''
    
    return cat('\n', *array, '\n')
#

def to_string(matrix, space1=None, space2=None):
    '''
        "Stringifies" a record (array or array of arrays) of strings: 
        One string (only) per line.
    '''
    
    if space1:
        if space2:
            return space1.join(space2.join(row) for row in matrix)
        else:
            return space1.join(matrix)
    else: 
        return ''.join(matrix)
    #
#

# We deal with paths:
# Given fragments, assembles them in a path
def get_path(*component):
    '''
        input: fragment(s) ${a}, ${b}, …
        output: The path ${a}/${b}/ …
        The function is fault-tolerant, in the sense that 
        every '//' is replaced with a '/' within the concatenation process.
    '''
        
    path = '/'.join(component)
    path += '/'
    path = path.replace('//', '/')
    return path
#

# LaTeX Markups: BEGINNING ---------------------------------------------------#
def def_path(name, path):
    '''
        LaTeX markup: define (\def) a path.
    '''
    
    return '\def\%s{%s}'%(name, path)
#
# LaTeX Markups: END----------------------------------------------------------#

# END

