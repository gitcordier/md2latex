import json 
import re
import mistune
import sys

from constants      import *
from md_extensions  import *
from log            import *
from utilities      import *
from constants      import *

__version__ = '1.0.0'
__author__ = 'Kavin Yao <kavinyao@gmail.com>, Gabriel Cordier <admin@gcordier.eu>'

def newline(func):
    '''Insert double newline at the beginning of string.'''
    def inner(*args, **argv):
        return '\n\n%s' % func(*args, **argv)

    return inner


class MetaRenderer(mistune.Renderer):
    '''Renderer used rendering meta section.

    The meta section is separated from main body by an hrule (---) and
    contains two parts:
    1. a first-level heading
    2. a list of metadata in the format: - <meta_key>: <meta_value>

    As a result, overriding the header and list* rendering methods is
    sufficient. autolink is also overriden to support email in author.'''

    def header(self, text, level, raw=None):
        return '\\def\\currenttitle{%s}\\title{\\currenttitle}' % text

    @newline
    def list(self, body, ordered=True):
        return '\\author{%s}' % body

    def list_item(self, text):
        _, meta_key, meta_val = re.split(r'^([^:]+):\s+', text, maxsplit=1)
        if meta_key != 'author':
            return ''

        authors = re.split(', +', meta_val.rstrip())
        return '\n\\and\n'.join(authors)

    def autolink(self, link, is_email=False):
        return r'\\\texttt{%s}' % link


class LatexRenderer(mistune.Renderer):
    '''Renderer for rendering markdown as LaTeX.

    Only a subset of mistune-flavored markdown is supported, which will be
    translated into a subset of LaTeX.'''

    FOOTNOTE = 'FTNT-MAGIC'

    use_block_quote = False
    use_enumerate = False
    use_hyperref = False

    def __init__(self):
        super(mistune.Renderer, self).__init__()
        self.footnotes_ = {}

    def not_support(self, feature):
        raise NotImplemented('%s is not supported yet.' % feature)

    # Fornow, you can't quote LaTeX code. LaTeX code will be compiled.
    # TODO: Find some workaround.
    @newline
    def block_code(self, code, lang=None):
        '''Ref: http://scott.sherrillmix.com/blog/programmer/displaying-code-in-latex/'''
        code = code.rstrip()
        return code
        #return '\\begin{verbatim}\n%s\n\\end{verbatim}' % code

    @newline
    def block_quote(self, text):
        '''Ref: http://tex.stackexchange.com/a/4970/43978'''
        self.use_block_quote = True
        return '\\begin{blockquote}%s\n\\end{blockquote}' % text

    def block_html(self, html):
        # !!
        self.not_support('Block HTML')
        #self.not_support('')

    @newline
    def header(self, text, level, raw=None):
        if level > 3:
            self.not_support('Header > 3')

        section = ('sub'*(level-1)) + 'section'
        return '\\%s{%s}' % (section, text)

    @newline
    def hrule(self):
        '''Ref: http://tex.stackexchange.com/a/17126/43978'''
        return r'\noindent\rule{\textwidth}{0.4pt}'

    @newline
    def list(self, body, ordered=True):
        if ordered:
            self.use_enumerate = True
            return '\\begin{enumerate}\n%s\\end{enumerate}' % body
        else:
            return '\\begin{itemize}\n%s\\end{itemize}' % body.replace(
                # TODO: Replace that with a renewcommand 
                '\item', 
                '\item[-]'
            )

    def list_item(self, text):
        return '    \\item %s\n' % text

    @newline
    def paragraph(self, text):
        return '%s' % text

    def table(self, header, body):
        self.not_support('Table')

    def table_row(self, content):
        self.not_support('Table')

    def table_cell(self, content):
        self.not_support('Table')

    def double_emphasis(self, text):
        '''Ref: http://tex.stackexchange.com/q/14667/43978'''
        return '\\textbf{%s}' % text

    def emphasis(self, text):
        return '\\emph{%s}' % text

    def codespan(self, text):
        return '\\texttt{%s}' % text

    def linebreak(self):
        return r'\\'

    def strikethrough(self, text):
        self.not_support('Strike-through text')

    def autolink(self, link, is_email=False):
        self.use_hyperref = True

        if is_email:
            return r'\href{mailto:%s}{%s}' % (link, link)
        else:
            return r'\url{%s}' % link

    def link(self, link, title, text):
        if 'javascript:' in link:
            # for safety
            return ''

        self.use_hyperref = True

        # title is ignored
        return r'\href{%s}{%s}' % (link, text)

    def image(self, src, title, text):
        self.not_support('Image')

    def raw_html(self, html):
        self.not_support('Inline HTML')

    def footnote_ref(self, key, index):
        # content will be patched later
        return '\\footnote{%s-%s}' % (self.FOOTNOTE, key)

    def footnote_item(self, key, text):
        # store footnotes for patch
        self.footnotes_[key] = text.strip()
        # return empty string as output
        return ''

    def footnotes(self, text):
        # return empty string as output
        return ''

###############################################################################
# The converter                                                               #
# FORK: BEGINNING ------------------------------------------------------------#
# Up to now this is where the fork is justified.                              #
# You may want to override this part                                          #
###############################################################################
class MarkdownToLatexConverter(LatexRenderer):
    
    def __init__(self, path, preferences):
        
        '''
            The .md file ${filename} must be at ${path}${filename}.
            preferences = the preferences, encoded as a json file.
        '''
        super().__init__()
        # 
        self.resolve = lambda name: path + name
        #
        try: 
            assert preferences not in NO
        except AssertionError:
            raise ValueError('No preferences file were submitted.') from None
        #
        try:
            pref = json.load(open(preferences, 'r')).items()
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError('Could not load the preferences files %s'%preferences) from None
        # 
        # Our preferences record. 
        self.preferences = dict((k, v) for k, v in pref if v not in FALSE)
    #
    
    meta_renderer = MetaRenderer()
    
    def convert(self, doc):
        try:
            meta, body = doc.split('---', 1)
        except ValueError:
            raise ValueError('Your document seems missing the meta part.')

    # ------------------------------------------------------------------------#
    # ------------------------------------------------------------------------#
        # The log system
        log = Log()
        
        # Title ----------------------#
        title = self.parse_meta(meta) #
        titlepage = '' # -------------#
        
        # Latex markup : begin and end a document -------------------------#
        BEGIN_DOCUMENT = '\setlength\parindent{0pt}\n\n\\begin{document}\n'#
        END_DOCUMENT = '\\end{document}\n' #-------------------------------#
        
        # DOCUMENTCLASS: BEGINNING -------------------------------------------#
        # Options for documentclass, as a dictionary
        if 'documentclass' in self.preferences:
            with open(self.resolve('documentclass.json'), 'r') as f:
                documentclass_standard = json.load(f)
            #
            try: 
                'class' in documentclass_standard
            except KeyError:
                raise KeyError('class is not declared.') from None
            #
            
            try: 
                'class' in self.preferences['documentclass']
            except KeyError:
                raise KeyError('class is not declared.') from None
            #
            
            documentclass_class = self.preferences['documentclass']['class']
            
            if documentclass_class in documentclass_standard['class']:
                pass
            else:
                log.add(LOG.NO_STANDARD_CLASS, documentclass_class)
            #
            # So now we are sure that a key 'documentclass', in both dicts.
            # We now deal with the options:
            
            if 'options' in self.preferences['documentclass']:
                documentclass_option_ = {
                    key: self.preferences['documentclass']['options'][key] 
                        for key in self.preferences['documentclass']['options'] 
                    if key not in FALSE
                }
                #documentclass_kind_and_options['class'] = documentclass_class
                
                # option must be a standard option of documentclass
                def set_documentclass_option(option):
                    
                    # Hence, there is no reason for the following step
                    # to end up as an exception. 
                    # If it does, then set_documentclass_option is not 
                    # used the way is was designed for.
                    try:
                        value = documentclass_option_[option]
                    except KeyError:
                        raise KeyError('ERROR: documentclass has no %s'%option)
                    
                    if option in documentclass_standard:
                        if value in documentclass_standard[option] + ['']:
                            pass
                        else:
                            log.add(LOG.OPTION, value, option)
                        #
                    #
                    else:
                        log.add(LOG.NO_OPTION, option)
                    #
                    return value
                
                #documentclass_class is already set.
                # documentclass: options 
                #ocumentclass_titlepage = documentclass_set('titlepage')
                #del documentclass_set('titlepage')
                
                option_ = {key: set_documentclass_option(key) 
                    for key in documentclass_option_
                }
                #
                    
                # We will need this later
                titlepage = option_['titlepage']
                
                # We will copy the options in the .tex file, as a single string
                # Before we do so, we include ', ' where necesssary.
                options_to_latex_file = [
                    '' if key =='class' or option_[key] in FALSE 
                    else str(option_[key]) + ', ' 
                    for key in option_
                ]
                
                # Optional, really. Just to clean up the end, so that we get 
                # '…]' instead of '…, ]'
                options_to_latex_file[-1] = options_to_latex_file[-1][:-2]
                
                documentclass = '\documentclass[%s]{%s}\n'%(
                    to_string(options_to_latex_file), 
                    documentclass_class
                )
            else:
                titlepage = ''
                documentclass = '\documentclass{%s}\n'%documentclass_class
                log.add(LOG.NO_OPTION_, documentclass_class)
            # 
            # Put everything together 
        # 'if documentclass' in self.preferences: END
        else:
            documentclass = ''
            documentclass_titlepage = ''
            log.add(LOG.NO_DOCUMENTCLASS)
        # DOCUMENTCLASS: END -------------------------------------------------#
        
        # Import packages: BEGINNING------------------------------------------#
        path_packages = self.resolve(self.preferences['import packages from'])
        packages_comment = '%: Import packages from ' + path_packages +'. '
            
        with open(path_packages, 'r') as f:
            # POLICY: We expect the file to be \n-terminated.
            #So, that's why we discard the last read character:
            packages_latex_markups = f.read()[:-1]
        
        packages = lines(
            '\n',
            packages_comment, 
            packages_latex_markups
        )
        #Import packages: END-------------------------------------------------#
        
        # Fonts : BEGINNING --------------------------------------------------#
        fonts_comment = '%: Fonts.'
        fonts_latex_markups = cat('\n', 
            '\defaultfontfeatures{Mapping=tex-text}',
            '\\newfontfamily{\\fw}{%s}',
            '\def\\fwfont{%s}', 
            '\def\mainfont{%s}',
            '\setmainfont{\mainfont}',
            '\\newfontfamily\mainfontLARGE[SizeFeatures={Size=%d}]{\mainfont}',
            '\\newfontfamily\mainfontLarge[SizeFeatures={Size=%d}]{\mainfont}',
            '\setmathfont(Latin)[Uppercase=Regular,Lowercase=Regular]{\mainfont}',
            '\setmathfont(Greek)[Uppercase=Regular,Lowercase=Regular]{\mainfont}',
            '\setmathrm{\mainfont}',
            '\setmathbb{\mainfont}'
        )%(
            self.preferences['fonts']['fixed_width'],
            self.preferences['fonts']['fixed_width'],
            self.preferences['fonts']['main'], 
            self.preferences['fonts']['LARGE'], 
            self.preferences['fonts']['Large']
        )
        fonts = lines(fonts_comment, fonts_latex_markups)
        # Fonts : END------ --------------------------------------------------#
        
        # Colors: BEGINNING --------------------------------------------------#
        if 'colors' in self.preferences:
            colors = self.preferences['colors'].items()
            html_colors_comment = '%: Define color'+ plural(colors) + '.'
            html_colors_latex_markups = lines(*(
                '\definecolor{%s}{HTML}{%s}'%(k, v) for k, v in colors))
            html_colors = lines(
                html_colors_comment, 
                html_colors_latex_markups
            )
        else: 
            html_colors = ''
        # Colors: END       --------------------------------------------------#
        
        # Language and more generally, language-dependent settings:BEGINNING--#
        if 'language' in self.preferences:
            language_dependent_settings_comment = \
                '%: Default language and dependent settings.'
            language_dependent_settings_latex_markups = cat('\n',
                '\setdefaultlanguage[]{%s}',
                '\\newcommand{\\currentdate}{%s}',
                '\def\\pagenumbering{%s}',
                '\def\\nametableofcontents{%s}',
            )%(
                self.preferences['language']['main'],
                self.preferences['language']['date'],
                self.preferences['language']['page numbering'],
                self.preferences['language']['table of contents']
            )
            language_dependent_settings = lines(
                language_dependent_settings_comment, 
                language_dependent_settings_latex_markups
            )
        #
        else:
            language_dependent_settings = ''
            log.add(LOG.LANGUAGE)
        #
        # Language and language-dependent settings: END ----------------------#
        # custom chapter, section, -------------------------------------------#
        if 'custom' in self.preferences:
            custom = self.preferences['custom']
            
            custom_level_comment = \
                '%: Custom (color, font,…) for section, subsection,….'
            # level = section, subsection, and so on
            
            # Nested function lang: ------------------------------------------#
            def lang(level, option):
                if option == 'color':
                    return '\\%sfont{\\color{%s}}'\
                        %(level, custom[level][option])
                #
                elif option == 'renewcommand':
                    return '\\renewcommand{\\the%s}{%s}'\
                        %(level, custom[level][option])
                #
                else:
                    log.add(LOG, level, option)
                    return LOG%(level, option)
            #-----------------------------------------------------------------#
            
            custom_level_latex_markups = to_string(((
                lang(level,option) for option in custom[level])
                for level in custom
           ), '\n', '\n')
            
        else:
            custom_chapter_section = ''
        
        custom_chapter_section = lines(
            custom_level_comment, 
            custom_level_latex_markups
        )
        # --------------------------------------------------------------------#
        # PATH(s) for sources (e.g. pictures): HERE --------------------------#
        # There is always a default path, which is ""= current folder.
        path_output_  = {'PATH_DEFAULT': def_path('PATHDEFAULT', '')}
        
        if 'sources' in self.preferences:
            # The default, as a string 'default', or 'default path'.
            # First we check if "sources" points to such default string.
            # In such case
            if str(self.preferences['sources']) in PATH_DEFAULT_:
                pass
            #
            # Where there are precise settings: Must be dict.-shaped.
            else:
                try: 
                    # img, misc, 
                    path_input_ = self.preferences['sources']
                    assert path_input_ != {}
                    
                    # POLICY: 
                    #   keys (path purpose)
                    #   no boolean, no default value
                    #   values (paths):
                    #   Same. No
                    set_aims    = set(path_input_.keys()) 
                    set_paths   = set(path_input_.values())
                    TROUBLE     = BOOLEAN | PATH_DEFAULT_
                    
                    trouble_with = dict(zip(('aims', 'paths'), (
                        set(x for x in _set if x in TROUBLE)
                        for _set in (set_aims, set_paths)
                    )))
                    
                    # POLICY: Key is off TRUE + FALSE + PATH_DEFAULT.
                    # Path can be '', ' ', '/', './'. In such case, it is
                    # interpreted as 'the current folder'.
                    POLICY_PATH_ROOT = ('', '/', './')
                    # So, we don't want any trouble:
                    # . aims: Set of all troubles must be the emptyset
                    # . paths: the same, excepted that the empty string is OK.
                    # (See the above policy)
                    are_aims_ok = trouble_with['aims'] == set() 
                    are_path_ok = trouble_with['paths'] <= {''}
                    is_ok       = are_aims_ok and are_path_ok
                    
                    assert is_ok
                #
                except AssertionError:
                    raise AssertionError('Since "sources" exists, only path are expected. No "True", "Yes", "default", …). Record must not be empty either!') from None
                #
                # We are forgiveful: We remove the useless spaces.
                def correct(path):
                    if ''.join(x for x in path if x!=' ') in POLICY_PATH_ROOT:
                        return ''
                    else: 
                        return path
                    #
                # correct: END
                    
                path_output_ = dict( # Keys are rewritten in a HR way.
                    (('PATH'+aim).replace(' ', '').upper(), correct(path)) 
                        for (aim, path) in path_input_.items()
                )
            #
        # i.e no source specified
        else: 
            # Dictionary path_output_ = default setting(s). Already done. So, 
            pass
        #
        path_comment = '%: Setting PATH.'
        path_latex_markups =  lines(*(cat('\n', 
            '% ' + k, def_path(k, get_path('../src', path_output_[k])))
                for k in path_output_))
        
        path = cat('\n', path_comment, path_latex_markups)
        
        # --------------------------------------------------------------------#
        # --------------------------------------------------------------------#
        # Pimp my page: BEGINNING --------------------------------------------#
        # Fancy package 
        if 'fancy' in self.preferences:
            fancy = self.preferences['fancy']
            
            try:
                YoN = fancy['Y/N']
                
                if YoN in TRUE:
                    pimp_my_page_comment = '%: Pimp my page: package fancy.'
                    
                    with open(self.resolve(fancy['path']), 'r') as f:
                        pimp_my_page_latex_markups = f.read()
                    #
                    pimp_my_page = lines(
                        pimp_my_page_comment, 
                        pimp_my_page_latex_markups
                    )
                #
                elif YoN in NO:
                    pimp_my_page = ''
                #
                else:
                    raise ValueError(to_string(('Preference "fancy": ', 
                            'Y/N must be either true or false.')))
                #
            except KeyError:
                raise KeyError('Preference "fancy": No value for "Y/N".') \
                    from None
        else: 
            custom_page_with_fancy_package = ''
        #
        # Pimp my page: END --------------------------------------------------#
        
        # Titlepage: BEGINNING -----------------------------------------------#
        # If notitlepage (see above)), then make_title := 'maketitle'
        # If titlepage, then the path of the title page is copied. 
        if titlepage == 'titlepage':
            if 'titlepage path' in self.preferences:
                # self.preferences['titlepage path'] must not be 'true'
                try: 
                    the_given_path = self.preferences['titlepage path']
                    
                    # We ensure that the path is a path, or at least, 
                    # looks like a path.
                    # Maybe later we'll perform a more accurate test
                    looks_like_a_path = the_given_path not in YES 
                    # and the given_path not in NO
                    
                    assert looks_like_a_path
                    #
                except AssertionError:
                    raise AssertionError(cat('', 'Path of title page: ', 
                        # So, this might not be the definitive version 
                        # of the following:
                        'You set titlepage path = %s. '%the_given_path,
                        'No boolean was expected. Only a path.'
                    ))
                #
                # So, 
                maketitle = '\n\input{../src/'+ the_given_path +'}\n'
                # NB. This replaces the title that is written in 'title!
            #
            else:
                maketitle = '\\maketitle'
            #
        elif titlepage == 'notitlepage':
            maketitle = ''
        else:
            maketitle = ''
        # titlepage: END -----------------------------------------------------#
        #                                                                     #
        # Foreword: BEGINNING ------------------------------------------------#
        if 'foreword' in self.preferences:
            foreword = self.preferences['foreword']
            try:
                YoN = foreword['Y/N']
            
            except KeyError:
                raise KeyError('Preferences: foreword has no Y/N option.') \
                    from None
            #
            try:
                assert YoN in BOOLEAN
            except ValueError:
                raise ValueError(cat('\n', 'Preferences: ', 
                        'the Y/N of "foreword" must be either ', 
                        'true or false.')) from None
            #
            if YoN in YES:
                with open(self.resolve(foreword['path']), 'r') as f:
                    foreword_latex_markups = f.read()
                #
                foreword_comment = '%: Foreword.'
                
                foreword = lines(
                    '\n',
                    foreword_comment, 
                    foreword_latex_markups, 
                    '\\newpage'
                )
            elif YoN in NO:
                foreword = ''
            #
            else:
                # This will not happen - see the above 'try'
                pass
        #
        else: 
            foreword = ''
        # Foreword: END ------------------------------------------------------#
        
        # Table of contents: BEGINNING ---------------------------------------#
        toc = ''
        if 'table of contents' in self.preferences:
            table_of_contents = self.preferences['table of contents']
            
            toc_latex_comment = '\n%: Table of comments (aka "toc").'
            
            try: 
                YoN = table_of_contents['Y/N']
            except KeyError:
                raise KeyError('Since "table of comments" exists, a key "Y/N" is expected') from None
            
            try:
                assert YoN in BOOLEAN
            except AssertionError:
                raise ValueError('table of comments: Y/N. Y/N Must be a boolean ("yes", true, "No", …)') from AssertionError    
            
            if YoN in YES:
                toc_latex_markups = '\\tableofcontents\\newpage'
            
                if 'renewcommand' in table_of_contents:
                    toc_latex_markup = cat('', 
                        toc_latex_markups, 
                        '\\renewcommand',
                        table_of_contents['renewcommand']
                    )
                #
            #
            elif YoN in NO:
                toc_latex_markups = ''
            #
            else:
                # This will not happen - see the above 'try'
                pass
            #
            toc = lines(toc_latex_comment, toc_latex_markups)
        else:
            toc = ''
        # Table of contents: END ---------------------------------------------#
        
        # Annex: BEGINNING ---------------------------------------------------#
        annex = ''
        if 'annex' in self.preferences:
            try:
                YoN = self.preferences['annex']['Y/N']
            except KeyError:
                raise KeyError('Since "annex" exists, a key "Y/N" is expected') from None
            
            try:
                assert YoN in BOOLEAN
            except AssertionError:
                raise ValueError('annex: Y/N. Y/N Must be a boolean ("yes", true, "No", …)') from AssertionError
            
            if YoN in YES:
                if 'path' in self.preferences['annex']:
                    the_given_path = self.preferences['annex']['path']
                    
                    # We now ensure that the path is a path, or at least, 
                    # looks like a path.
                    # TODO: (?) Maybe later we'll perform a more accurate test.
                    looks_like_a_path = the_given_path not in BOOLEAN
                    
                    try:
                        assert looks_like_a_path
                        #
                    except AssertionError:
                        raise AssertionError(cat('', 'Path for annex: ', 
                            # So, this might not be the definitive version 
                            # of the following:
                            'You set annex path = %s. '%the_given_path,
                            'No boolean was expected. Only a path.'
                        ))
                    annex = '\input{../src/%s}'%the_given_path
                
                    if 'section' in self.preferences['annex']:
                        annex += '\\renewcommand{\\thesection}{' \
                        + self.preferences['annex']['section']['renewcommand']\
                        + '}\n'
                    else:
                        pass
                else:       # i.e no path for annex
                    pass
            elif YoN in NO: # idem
                annex = ''
            #
            else:
                # This will not happen - see the above 'try'
                pass
        else:  # i.e. no annex
            annex = ''
        #
        # Annex: END ---------------------------------------------------------#
        # Put everything together.
        body = self.parse_body(clean_up(copy_all_inputmd(body)))
         # UGLY but it works…
        body = body.replace('1729ampersand', '&')
        body = body.replace('√', '\\')
        #
        body = body.replace('\¢--', COMMENTCODESTARTS)
        body = body.replace('\--¢', COMMENTCODEENDS)
        #body = body.replace('XeLaTeX', '\XeLaTeX{}') # TODO: regex
        #body = body.replace('LaTeX', '\LaTeX{}')
        
        # Remove some slang. TODO: As parameters, in the JSON prefs. file ? 
        body = body.replace('iff', 'if and only if')
        body = body.replace('iif', 'if and only if')
        body = body.replace('\if and only if', '\iff')
        # So that complex LaTex stuffs like \begin{align}… work. 
        # This is lame patching. It does not provide any garantee that 
        # LaTeX code is well-formed.
        body = body.replace('%\n\n', '%\n')
        body = body.replace('\\\n\n', '\\\n')
        body = body.replace('\n\end', '\end')
        body = body.replace('%\n\n', '%\n%')
        
        return dict(tex=dict([
                ('documentclass', documentclass), 
                ('packages', packages), 
                ('fonts', fonts),
                ('html colors', html_colors), 
                ('language-dependent settings', language_dependent_settings),
                ('path variable(s)', path),
                ('custom chapter section', custom_chapter_section),
                ('pimp my page', pimp_my_page),
                ('resolved commands', self.resolve_commands()),
                ('title', title),
                ('begin document', BEGIN_DOCUMENT), 
                ('maketitle', maketitle),
                ('foreword', foreword),
                ('toc', toc),
                ('body', body),
                ('annex', annex),
                ('end document', END_DOCUMENT)
        ]),log=log)
    # ------------------------------------------------------------------------#
    # ------------------------------------------------------------------------#
# ----------------------------------------------------------------------------#
###############################################################################
# FORK: END ------------------------------------------------------------------#
###############################################################################
    def parse_meta(self, meta):
        md = mistune.Markdown(renderer=self.meta_renderer)
        return md.render(meta)

    def parse_body(self, content):
        md = mistune.Markdown(renderer=self)
        return self.resolve_footnotes(md.render(content))

    ### The following commands use properties set in LatexRenderer

    def resolve_footnotes(self, text):
        parts = re.split(r'%s-([^}]+)' % self.FOOTNOTE, text)
        new_parts = []
        for i, part in enumerate(parts):
            if i%2 == 0:
                # normal part
                new_parts.append(part)
            else:
                # footnote part
                new_parts.append(self.footnotes_[part])

        return ''.join(new_parts)

    def resolve_packages(self):
        pass

    def resolve_commands(self):
        if True: #self.use_block_quote:
            return r'''
\newenvironment{blockquote}{%
  \par%
  \medskip
  \leftskip=4em\rightskip=2em%
  \noindent\ignorespaces}{%
  \par\medskip}
'''
        else:
            return ''

