----------------------- MODULE Md2LaTeXSystemDesignPreferencesFile ------------
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* So, here is the specification of a file NAME.preferences.json .     *)
(* Such a file must implement, or at least "follow", a specific policy,*)
(* that I named "YesOrNo".                                             *)
(* Further explanations in Md2LaTeXSystemDesignPreferences.            *)
(*                                                                     *)
(* This file is only here for the sake of completeness;                *)
(* DOMAIN_OF_PREFERENCES and SET_OF_PREFERENCES are currently set as   *)
(* CONSTANTS.                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* NAME stands for the project's name.                                 *)
(* The naming convention (but it is off specs) is                      *)
(* NAME.md.pdf: The pdf output, md stands for 'main document' -        *)
(* think of it as a main function in a C programm.                     *)
(* NAME.md.md:The markdown main document (recursive imports are allowed*)
(* NAME. preferences.json: the preferences file                        *)     
(* and so on.                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

\* The preferences as a mapping:
\* First, Domain:
 DOMAIN_OF_PREFERENCES == {
    "documentclass",
    "import_packages", 
    "fancy",            \* To overwrite default settings
    "import_titlepage", \* make your own page
    "table_of_contents",
    "fonts",            \* XeLaTeX: Any font managed by the OS is OK.
    "colors",
    "language",         \* Encompasses all language-dependent settings.
    "custom",           \* Misc. settings, e.g. section color
    "foreword",
    "annex",
    "sources",          \* Additional path, e.g. /src/img
}

\* Next, the function space:
SET_OF_PREFRENCES == [
    documentclass:[
        class: STRING_ALPH_NONEMPTY, 
        options: [
            paper_size: STRING_ALPH ,
            draft_mode: {"draft", ""},
            titlepage:{"titlepage", "notitlepage", ""}]],
    import_packages: [
        Y_N: JSON_BOOL, 
        path: ANY],
    fancy: [
        Y_N: JSON_BOOL, 
        path:{"NAME.fancy.tex", ""}],
    import_titlepage: [
        Y_N: JSON_BOOL, 
        path: PATH],
    table_of_contents: [
        Y_N: JSON_NO \cup JSON_YES, 
        renewcommand: STRING_LATEX],
    fonts: [
      main: STRING_ALPH_NONEMPTY,
      fixed_width: STRING_ALPH_NONEMPTY,
      LARGE: NAT,
      Large: NAT],
    (* 'colors' is a record of \definecolor{}{HTML}{}*)
    colors: [
        Y_N: JSON_BOOL, 
        definition: RECORD],
    language: [
      main: STRING_ALPH_NONEMPTY,
      date: STRING_LATEX,
      page_numbering: STRING_ALPH ,
      nameForTableOfContents: STRING_ALPH],
    custom:  [
      section:  [
        color: STRING_ALPH,
        renewcommand: STRING_LATEX],
      subsection:  [
        renewcommand: STRING_LATEX]],
    foreword: [
      Y_N: JSON_BOOL,
      path: {"$AME.foreword.tex", ""}],
    annex: [
      Y_N: JSON_BOOL, 
      section:  [
        renewcommand: STRING_ALPH],
      path: {"NAME.annex.tex", ""}], 
    sources: [
      root: {"./"},
      images: {"img"}]
]


===============================================================================