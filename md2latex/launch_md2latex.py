#!/usr/bin/env python

import sys
import md2latex
from utilities import lines
'''
/Users/Shared/doc/ot/ot_specs'''
if len(sys.argv) < 4:
    print(sys.stderr, 'Usage: md2latex name preferences')
    sys.exit(1)

path        = sys.argv[1]
name        = sys.argv[2]
md          = name + '.md'
log_file    = name + ".conversion.log"
preferences = sys.argv[3]

with open(path + md, 'r') as f:
    converter = md2latex.MarkdownToLatexConverter(path, preferences)
    dct = converter.convert(f.read())
#

with open(path + name + '.tex', 'w') as tex:
    [tex.write(dct['tex'][key]) for key in (
        'documentclass',
        'packages', 
        'fonts', 
        'html colors',
        'language-dependent settings',
        'path variable(s)',
        'custom chapter section',
        'pimp my page',
        'resolved commands',
        'title',
        'begin document',
        'maketitle',
        'foreword',
        'toc',
        'body',
        'annex',
        'end document'
    )]
    
#

with open(path + log_file, 'w') as log:
    OK = 'Everything went well.'
    if len(dct['log']) == 0:
        log.write(OK)
        print(OK)
    else:
        [log.write(lines(*x)) for x in dct['log'].values()]
        print('Maybe is it OK but you have warning(s). Check the .conversion.log file.')
#

print("Done.")