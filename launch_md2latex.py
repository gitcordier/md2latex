#!/usr/bin/env python

import sys
import md2latex
'''
/Users/Shared/doc/ot/ot_specs'''
if len(sys.argv) < 4:
    print(sys.stderr, 'Usage: md2latex path name preferences')
    sys.exit(1)

path = sys.argv[1]

# If path is not '/'-terminated, then we insert a '/'.
sep = '' + (path[-1] != '/')*'/'

name_of_the_md_file = path + sep + sys.argv[2] # path/name
preferences_json    = path + sep + sys.argv[3] # path/preferences.json

with open(name_of_the_md_file, 'r') as the_md_file:
    ''' input: path and preferences
        output: the latex version, as a string.
    '''
    converter = md2latex.MarkdownToLatexConverter(
            path, 
            preferences=preferences_json
    )
    latex = converter.convert(the_md_file.read())

#if len(sys.argv) == 2:
    #print latex
with open(name_of_the_md_file + '.tex', 'w') as out:
    '''
        write the conversion result into a .tex file.
    '''
    out.write(latex)

print("Done.")