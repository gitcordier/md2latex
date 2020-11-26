
BEGINNING = '\\begin{document}'
CLOSING = '\\end{document}'
COMMENT_OPENING = 'LaTeXComment1729 %s: BEGINNING'
COMMENT_CLOSING = 'LaTeXComment1729 %s: END\n\n'

BASE = 'Md2LaTex%s'
file_ = (
    'Correctness', 
    'SystemDesign',
    'Algorithms',
    'Specifications',
    'SystemDesignPreferencesFile'
)

with open(BASE%'SpecificationsAll.tex', 'w') as g:
    for e in file_:
        filename = BASE%e + '.tex'
        with open(filename, 'r') as f:
            #g.write('%')
            s = f.read()
            i = s.find(BEGINNING)
            j= s.find(CLOSING)
            s = COMMENT_OPENING%filename \
                +  s[i+ len(BEGINNING): j] \
                + COMMENT_CLOSING%filename
            s=s.replace('LaTeXComment1729', '%. ')
            # Workaround to avoid quirk with XeLaTeX:
            s=s.replace("\\.{'}", "^{\prime}")
            s=s.replace('\.', '\,')
            g.write('\\newpage\n' + s + '\n')
        #
    #
    