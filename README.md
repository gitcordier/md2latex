md2latex
========

A lame Markdown to LaTeX / XeLaTex converter.
This is a fork of the Kavin Yao's md2latex, available at 
  [https://github.com/kavinyao/md2latex](https://github.com/kavinyao/md2latex "Kavin Yao's Github").

You can also get this original parser with a ``pip install md2latex`` (use ``sudo`` if necessary).

**Bear in mind that both versions of md2LaTeX depend on an older (0.2) version of [mistune](https://github.com/lepture/mistune "Mistune").**

Test
-------

In doc/: See``src/md2latex_doc.md.md`` for an example and run ``bash *run*`` to taste a flavor of it.

Features
--------

- title
- other standard documentclass options
- titlepage
- author(s)
- headings (converted to sections)
- lists (converted to enumerate/itemize)
- emphasis, strong and monospace text style
- hyperlink (using ``hyperref`` package)
- footnote (in mistune syntax)
- HTML colorts
- HTML comments (converted to LaTeX comments, with the TeXShop convention "%:")
- Input files markups (converted to LaTeX \input 's)
- Language and graphic design settings (fonts, colors, section, …)
- LaTeX code: Tables, mathematical formulas 
- Foreword
- Annex
- Table of contents
- Export as pdf (use the bash script)

Caveats
-------
You can inline LaTeX commands because they are not markdown-parsable. However, md2latex does not do auto-escaping for you so if you have underscore LaTeX meta characters such as _ or % in your document, be cautious!
If a mathematical command is sophisticated, e.g. \begin{align} …, then the latex compilation could break, for empty-line-inserted reason. 
For now, workarounds are:

- Clean up the LateX output;
- Go back to LaTeX  source codes…  
  It's all about trade-offs… If you want to type pure AMSTeX, then a *TeX could be the best option.
- Import content from a .tex file, with the inputmd command.  
  **I used this a lot (inserting complex tables). It works very well.**


Documentation
-------
The full manual (see doc/src/md2latex_doc.md.md``) is … being written. A fancy term for: there is currently no full manual.

doc/TLA encloses the (partial) specs of the parse.  
It is ongoing but you will nevertheless get the very format of the preferences file. 
Hence, I think it may provide a great deal of help. 
I have put everything together [here](https://github.com/gitcordier/md2latex/tree/master/doc/TLA/pdf).
Enjoy!


Acknowledgement
---------------

Thanks to @kavinyao for the great job.

Thanks @lepture for the super awersome [mistune](https://github.com/lepture/mistune "Mistune") markdown parser.

