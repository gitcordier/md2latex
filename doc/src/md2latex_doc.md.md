# Markdown to \LaTeX or \XeLaTeX Test Document

- author: Git Cordier <admin@gcordier.eu>

---
<!-- Some LaTeX commands . TODO: md2latex.py 
\renewcommand{\words}[1]{#1$^\ast$} -->

<!-- Content: BEGINNING -->
\newcommand{\vardoc}[1]{\$\{#1\}}
# Introduction: Why I do this, by Kavin Yao
\inputmd{src/content/why_i_do_this.md}

<!-- Content: END -->

# Why I do this
 
# What is mapped (and what is not)

what is mapped LateX code (math) case 
The current line was typeset from \LaTeX {\fw commands}, 
including AMS ones: $12^3 + 1^3 = 1729 = 9^3 + 10^3$. You can also use environments, e.g.
\begin{align}e^{i\pi} +1 = 0\end{align}

TODO 
summary as a table
\inputmd{src/content/table/md2latex_doc.mapping.tex}
not mapped = color/ font of a given piece of characters (see title!)
By the very definition of what md is, i don' t see any complete mapping
workaround: defining commands = language extensions, like what we do with inputmd

# comment
note that comment may start with %: . So that TeXShop users can get the document structure

## XeLaTeX or LaTeX?

I use \XeLaTeX, which is \XeTeX compiling \LaTeX code.
From the [{{\XeTeX{}}}](https://en.wikipedia.org/wiki/XeTeX "{{\XeTeX{}}} wikipedia page") wikipedia page:

> {{\XeTeX{}}} is a {{\TeX{}}} typesetting engine using Unicode and supporting modern font technologies […]. 
> It was originally written by Jonathan Kew and is distributed under the X11 free software license.

> It natively supports Unicode and the input file is assumed to be in UTF-8 encoding by default. 
> **XeTeX can use any fonts installed in the operating system without configuring TeX font metrics**[…].

This is the reason why I use \XeLaTeX {{$\uparrow$}}.

<!-- Euler's identity -->
<!-- breaking lines brings trouble: TODO-->
\begin{align}  e^{i\pi} + 1 = 0  \end{align}

<!-- For now you cant nest \¢-- inside \© markups-->
\¢--
% Euler's identity
\begin{align} 
  e^{i\pi} + 1 = 0.
\end{align}
\--¢
# General policy
Either you don't say it, either you say it clearly
it is true iff it is explicitely stated that it is true

\inputmd{src/content/table/md2latex_logic.tex}
no = false, yes = true

no = $\emptyset$, False, false
# naming conventions
## paths 
## keys

\inputmd{src/content/table/md2latex_doc.keys.tex}


### Y/N
## files
### md to *tex
### log
### script
# The structure of a md2latex
\inputmd{src/content/table/md2latex_content.tex}


## Root 

### {\fw \vardoc{name}.run.sh}
{\color{orange}{{@}{\fw optional}}}

### {\fw \vardoc{name}.preferences.json}
{\color{red}{{@}{\fw !optional}}}

## {{\fw src}} 
{\color{red}{{@}{\fw !optional}}}

### {{\fw content/}}
{\color{orange}{{@}{\fw optional}}}

### {{ \fw documentclass}}
{\color{orange}{{@}{\fw optional}}}
{\color{green}{{@}{\fw standard}}}

### {{ \fw img}}
{\color{orange}{{@}{\fw optional}}}


## {{ \fw dst}}
{\color{red}{{@}{\fw !optional}}}


# Next
# The implementation
## The parser
### Case HTML comments
## The writer
## Utilities
### HTML Comments

---