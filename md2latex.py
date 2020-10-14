import json 
import re
import mistune
#from varname import nameof

__version__ = '0.0.2'
__author__ = 'Kavin Yao <kavinyao@gmail.com>'
__all__ = ['MarkdownToLatexConverter']

def newline(func):
    """Insert double newline at the beginning of string."""
    def inner(*args, **argv):
        return '\n\n%s' % func(*args, **argv)

    return inner


class MetaRenderer(mistune.Renderer):
    """Renderer used rendering meta section.

    The meta section is separated from main body by an hrule (---) and
    contains two parts:
    1. a first-level heading
    2. a list of metadata in the format: - <meta_key>: <meta_value>

    As a result, overriding the header and list* rendering methods is
    sufficient. autolink is also overriden to support email in author."""

    def header(self, text, level, raw=None):
        return '\\title{%s}' % text

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
    """Renderer for rendering markdown as LaTeX.

    Only a subset of mistune-flavored markdown is supported, which will be
    translated into a subset of LaTeX."""

    FOOTNOTE = 'FTNT-MAGIC'

    use_block_quote = False
    use_enumerate = False
    use_hyperref = False

    def __init__(self):
        super(mistune.Renderer, self).__init__()
        self.footnotes_ = {}

    def not_support(self, feature):
        raise NotImplemented('%s is not supported yet.' % feature)

    @newline
    def block_code(self, code, lang=None):
        """Ref: http://scott.sherrillmix.com/blog/programmer/displaying-code-in-latex/"""
        code = code.rstrip()
        return '\\begin{verbatim}\n%s\n\\end{verbatim}' % code

    @newline
    def block_quote(self, text):
        """Ref: http://tex.stackexchange.com/a/4970/43978"""
        self.use_block_quote = True
        return '\\begin{blockquote}%s\n\\end{blockquote}' % text

    def block_html(self, html):
        self.not_support('Block HTML')

    @newline
    def header(self, text, level, raw=None):
        if level > 3:
            self.not_support('Header > 3')

        section = ('sub'*(level-1)) + 'section'
        return '\\%s{%s}' % (section, text)

    @newline
    def hrule(self):
        """Ref: http://tex.stackexchange.com/a/17126/43978"""
        return r'\noindent\rule{\textwidth}{0.4pt}'

    @newline
    def list(self, body, ordered=True):
        if ordered:
            self.use_enumerate = True
            return '\\begin{enumerate}\n%s\\end{enumerate}' % body
        else:
            return '\\begin{itemize}\n%s\\end{itemize}' % body

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
        """Ref: http://tex.stackexchange.com/q/14667/43978"""
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

# The converter.
class MarkdownToLatexConverter(LatexRenderer):
    def __init__(self, path, preferences=None):
        
        '''
            path: If path is PATH, then the .md file FILE must be at PATH/FILE.
            preferences = the preferences, encoded as a json file, 
                say PREFERENCES.json.
                Such file must be at PATH/PREFERENCES.json
        '''
        
        super().__init__()
        self.path = path
        if preferences is None:
            pass
        elif len(preferences) == 0: 
            pass
        elif preferences == 'default':
            pass
        else:
            self.VALUES_FOR_TRUE = (True, "true", "True")
            self.VALUES_FOR_FALSE = (None, '', False, 'false', "False")
            
            pref = json.load(open(preferences, 'r')).items()
                
            self.preferences = dict(
                (k, v) for k, v in pref if v not in self.VALUES_FOR_FALSE
            )
            
    def get_path_from_key(self, key):
        return '/'.join((self.path, self.preferences[key]))
            
    
    meta_renderer = MetaRenderer()
    
    def convert(self, doc):
        try:
            meta, body = doc.split('---', 1)
        except ValueError:
            raise ValueError('Your document seems missing the meta part.')

# ----------------------------------------------------------------------------#
        
        title = self.parse_meta(meta)
        
        # UGLY
        displaytitle = '\def\displaytitle{%s}'%title[7: -1]
        
        def get_documentclass_option(key):
            value = self.preferences['documentclass'][key]
            
            if value in self.VALUES_FOR_FALSE:
                return ''
            elif value in self.VALUES_FOR_TRUE:
                return key
            else:
                return value
            #
        #        
        documentclass =  '\\documentclass[%s]{%s}'%(','.join((
                        get_documentclass_option('frame'), 
                        get_documentclass_option('fonts_default_size'), 
                        get_documentclass_option('titlepage'), 
                        get_documentclass_option('openany') )), 
                        get_documentclass_option('kind')
        )
        
        # Import packages
        with open(self.preferences['import_packages_from'], 'r') as f:
            packages = f.read()
        
        # Fonts 
        font_ = self.preferences['fonts']
        
        with open('fonts.txt', 'r') as f:
            fonts = f.read()%(
                font_['fixed_width'],
                font_['main'], 
                font_['LARGE'], 
                font_['Large']
            )
        
        # Colors
        color_ = self.preferences['colors']
        colors = '\n'.join('\definecolor{%s}{HTML}{%s}'%(k, v) 
            for k, v in color_.items())
        
        language = '\setdefaultlanguage[]{%s}'%self.preferences['language']
        
        # @optional
        # Fancy package 
        if 'fancy' in self.preferences.keys():
            fancy = open(self.get_path_from_key('fancy'), 'r').read()
        else: 
            fancy = ''
        
        # Title page
        if self.preferences['documentclass']['titlepage'] is True:
            if self.preferences['titlepage'] in {None, False, ''}:
                maketitle = '\\maketitle'
            else:
                with open(self.preferences['titlepage'],'r') as f:
                    maketitle = f.read()
        else:
            maketitle = ''
        
        # custom chapter, section, 
        custom_ = self.preferences['custom']
        
        _ = []
        for level in custom_:
            dct = custom_[level]
            
            if 'color' in dct:
                _.append('\\%sfont{\\color{%s}}'%(
                    level, 
                    dct['color']
                )
            )
            
            if 'renewcommand' in dct:
                _.append('\\renewcommand{\\the%s}{%s}'%(
                    level, 
                    dct['renewcommand']
                )
            )
        
        custom = '\n'.join(_)
        
        # Introduction
        with open(self.preferences['foreword'], 'r') as f:
            foreword = f.read() + '\\newpage'
        
        # Table of contents
        toc_ = self.preferences['table_of_contents']
        _ = []
        if 'renewcommand' in toc_:
            _.append('\\renewcommand%s'%toc_['renewcommand'])
        
        _.append('\\tableofcontents\\newpage')
        
        toc = '\n'.join(_)
        
        # @optional
        # Annex
        if 'annex' in self.preferences.keys():
            annex = '\input{%s}'%(self.preferences['annex']).split('/')[-1]
        else:
            annex = ''
        
        return '\n\n'.join((
            documentclass,
            packages, 
            fonts, 
            colors,
            language,
            displaytitle,
            custom,
            fancy,
            self.resolve_commands(),
            title,
            '\setlength\parindent{0pt}\n\\begin{document}',
            maketitle,
            foreword,
            toc,
            self.parse_body(body),
            annex,
            '\\end{document}'
        ))
# ----------------------------------------------------------------------------#
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
            return r"""
\newenvironment{blockquote}{%
  \par%
  \medskip
  \leftskip=4em\rightskip=2em%
  \noindent\ignorespaces}{%
  \par\medskip}
"""
        else:
            return ''

