----------------- MODULE Md2LaTeXCorrectness ----------------------------------

(* The preferences must be an element of SET_OF_PREFERENCES.           *)
(* They must be univoquely encoded in a preferences file.              *)
(* Conversely, the format of such file is the mappings space           *)
(* SET_OF_PREFERENCES.                                                 *)
(*                                                                     *)
(* The current module specifies the preferences file.                  *)  
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
         
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Since this module should be read first, we declare global naming    *)
(* conventions:                                                        *)
(*                                                                     *)                                                                             
(* NAME stands for the project's name.                                 *)
(* The naming convention (but it is off specs) is                      *)
(* NAME.md.pdf: The pdf output, md stands for 'main document' -        *)
(* think of it as a main function in a C programm.                     *)
(* NAME.md.md: The markdown main document (recursive imports are OK    *)
(* NAME. preferences.json: the preferences file                        *)     
(* and so on.                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* So, here is the specification of a file NAME.preferences.json .     *)
(* Such a file must implement, or at least "follow", a specific policy,*)
(* that I named "YesOrNo".                                             *)
(* Such a policy is istancied with                                     *)
(*     DOMAIN_OF_PREFERENCES and                                       *)
(*     SET_OF_PREFERENCES.                                             *)
(*                                                                     *)
(* Further explanations below.                                         *)
(*                                                                     *)
(* This file only exists for the sake of readability,                  *)
(* DOMAIN_OF_PREFERENCES and SET_OF_PREFERENCES should be regarded as  *)
(* CONSTANTS.                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(*                                                                     *)
(* The YesOrNo policy:                                                 *)
(* Goal: The very purpose of all that verbose is about implementing a  *)
(* key -namely, "Y/N" - you can see as a switch on/off button.         *)
(*                                                                     *)
(* Definitions:                                                        *)
(* 'Yes' or 'No' is always about a sequence of logical action(s).      *)
(* encoded as a dictionary value.                                      *)
(* 1. No: Means "no action"; which we define as follows:               *)
(*        i. If you do something, then it is discarded.                *)
(*        ii.If you announce something, then it is disregarded.        *)
(* 2. Saying "No": The current key is mapped to some value in JSON_NO. *)
(* 3. Saying "Yes":The current key is mapped to some value in JSON_YES.*)
(*                                                                     *)
(* Statements:                                                         *)
(* 1. It is only Yes XOR No (see above definitions 2, 3).              *)
(* 2. You say it once, whith a single value.                           *)
(* 3.1.1. If you do not say anything, then it is No.                   *)
(* 3.1.2. If you say "emptyset" (None, NULL, "", …), then it is No.    *)
(* 3.1.3. If you say "No", then it is No.                              *)
(* 3.2. If you say "Yes", then you do 'value for key' right now.       *)
(*                                                                     *)
(* Implementation                                                      *)
(* The "yes or no" key Y_N                                             *)
(*    (see Statement 1 for existence, Statement 2 for uniqueness)      *)
(* is always the String "Y/N".                                         *)
(* Moreover, we expect you to actually do something relevant/nontrivial*)
(* This latter requirement cannot be implemented from a general case,  *)
(* since:                                                              *)
(* (a) "relevant" and "nontrivial" are context-dependent.              *)
(* (b) The context space is infinite.                                  *)
(* A complementary approach is about defining                          *)
(*     EXCLUDED_BY_YES_OR_NO_POLICY                                    *)
(* as the minimal set of what is either trivial or irrelevant.         *)
(* This set is not constructed ;) .                                    *)
(*    (In practice, EXCLUDED_BY_YES_OR_NO_POLICY should contain,       *)
(*     at least, boolean and numerical values).                        *)
(* Hence, we cannot guarantee that the YesOrNo policy is implemented.  *)
(* But we can check that the policy is "followed", in the sense that:  *)
(* i. The policy is partially implemented and:                         *)
(* ii.If the provided content is actually relevant,                    *)
(*         then the policy is (nonprovably) implemented.               *)
(*                                                                     *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

CONSTANTS PATH            \* Any path 
CONSTANTS 
    STRING_ALPH,          \* The words of the alphabet {a, …,z, A, …, Z}. 
    STRING_ALPH_NONEMPTY, \* == STRING_ALPH \{""}
    STRING_LATEX          \* All LaTeX Markups/commands, including "".

CONSTANT HTML_COLORS      \* The set of of all dictionaries 
                          \* {(k,v)} where every evaluation 
                          \*     \definecolor{k}{HTML}{v} 
                          \* sets a HTML color in LaTeX.
                          
CONSTANT NAT              \* {0, 1, 2, …}
CONSTANT EXCLUDED_BY_YES_OR_NO_POLICY

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* JSON_X: Set of all possible encoding(s) of x in a JSON file.        *)
(* "yes", "on", and "true" are synonyms;                               *)
(* "no", "off", and "false" are synomyms.                              *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
CONSTANTS JSON_BOOL, JSON_NO, JSON_YES, Y_N


\* The preferences as a mapping:
\* First, Domain:
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* A compliant set of preferences is a necessarily (=>)                *)
(* i. A mapping of domain DOMAIN_OF_PREFERENCES;                       *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
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
    "sources"          \* Additional path, e.g. /src/img
}

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Bear in mind that it is all about MAPPINGS: The domain is rigid,    *)
(* it is always the same DOMAIN_OF_PREFERENCES, which means that       *)
(* every key from DOMAIN_OF_PREFERENCES must exist in the record.      *)
(* Hence, they is NO OPTIONAL KEY.                                     *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

\* Next, the function space:
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* A compliant set of preferences is a necessarily (=>)                *)
(* i. A mapping of domain DOMAIN_OF_PREFERENCES, more specifically:    *)
(* ii. An element of SET_OF_PREFERENCES, see below.                    *)
(* In practice, the converse of (ii) is not true, since we expect some *)
(* common sense, e.g. setting fonts.LARGE > fonts.large.               *)
(* But common sense is off scope.                                      *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

SET_OF_PREFERENCES == [
    documentclass:[
        class: STRING_ALPH_NONEMPTY, 
        options: [
            paper_size: STRING_ALPH ,
            draft_mode: {"draft", ""},
            titlepage:{"titlepage", "notitlepage", ""}]],
    import_packages: [
        Y_N: JSON_BOOL, 
        path: PATH],
    fancy: [
        Y_N: JSON_BOOL, 
        path:{"NAME.fancy.tex", ""}],
    import_titlepage: [
        Y_N: JSON_BOOL, 
        path: PATH],
    table_of_contents: [
        Y_N: JSON_BOOL, 
        renewcommand: STRING_LATEX],
    fonts: [
      main: STRING_ALPH_NONEMPTY,
      fixed_width: STRING_ALPH_NONEMPTY,
      LARGE: NAT,
      Large: NAT],
    colors: [
        Y_N: JSON_BOOL, 
        definition: HTML_COLORS],
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
      path: {"NAME.foreword.tex", ""}],
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


