md2latex
========

A lame Markdown to LaTeX / XeLaTex converter.
This is a fork of the Kavin Yao's md2latex, available at 
  [https://github.com/kavinyao/md2latex](https://github.com/kavinyao/md2latex "Kavin Yao's Github").

You can also get this original parser with a ``pip install md2latex`` (use ``sudo`` if necessary).


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
- HTML comments (converted to LaTeX comments, with the TeXShop convention "%:")
- Input files markups (converted to LaTeX \input 's)
- Language and graphic design settings (fonts, colors, section, …)
- Foreword
- Annex
- Table of contents
- Export as pdf (use the bash script)

Caveats
-------

You can inline LaTeX commands because that are not markdown-parsable. However, md2latex does not do auto-escaping for you so if you have underscore LaTeX meta chracters such as _ or % in your document, be cautious!

Acknowledgement
---------------

Thanks to @kavinyao for the great job.

Thanks @lepture for the super awersome mistune_ markdown parser.

.. _mistune: [https://github.com/lepture/mistune](https://github.com/lepture/mistune "Mistune")
