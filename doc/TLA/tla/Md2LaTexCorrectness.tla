------------------------ MODULE Md2LaTeXCorrectness ---------------------------
EXTENDS FiniteSets

CONSTANTS ANY, PATH \* Any object, any path
CONSTANTS 
    STRING_ALPH, \* The words of the latin alphabet
    STRING_ALPH_NONEMPTY, \* == STRING_ALPH \{""}
    STRING_LATEX \* All LaTeX Markups/commands, including "".
CONSTANT RECORD  \* Any record
CONSTANT NAT     \* Any integer 0, 1, 2, …
\* The preferences define a unique record
CONSTANTS DOMAIN_OF_PREFERENCES, SET_OF_PREFERENCES

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* "yes", "on", and "true" are synonyms;                               *)
(* "no", "off", and "false" are synomyms.                              *)
(* The way we express "yes", "no" in a JSON file.                      *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
CONSTANTS Y_N, JSON_YES, JSON_NO, EXCLUDED_BY_YES_OR_NO_POLICY

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* The preferences are identified with a file 'preferences'.           *)
(* In practice, this is a JSON file NAME.preferences.json               *)
(*     (see CONSTANT SET_OF_PREFERENCES),                              *)
(* even if no semantics push on that.                                  *)
(*                                                                     *)
(* isPreferencesFileCompliant keeps track of preferences compliance.   *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
VARIABLES preferences, isPreferencesFileCompliant

(* Convenient operators.                      *)
(* Recall that Yes = True and that No = False *)
JSON_BOOL == JSON_YES \cup JSON_NO
XOR(a, b) == (a \/ b) /\ (~b \/ ~a)

(* YesOrNo policy: BEGINNING ------------------------------------------------*)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* So, here is the specification of a file NAME.preferences.json .      *)
(* See CONSTANTS DOMAIN_OF_PREFERENCES, SET_OF_PREFERENCES;            *)
(*     or Md2LaTeXSystemDesignPreferencesFile                          *)
(* Such a file must implement, or at least "follow", a specific policy,*)
(* that I named "YesOrNo".                                             *)
(*                                                                     *)
(* The YesOrNo policy:                                                 *)
(* Goal: The very purpose of all that verbose is about implementing a  *)
(* key -namely, Y_N - you can see as a switch on/off button.           *)
(*                                                                     *)
(* Definitions:                                                        *)
(* 1. No: Means "no action"; which we define as follows:               *)
(*        i. If you do something, then it is discarded.                *)
(*        ii.If you announce something, then it is disregarded.        *)
(* 2. Saying "No": The current key is mapped to some value in JSON_NO. *)
(* 3. Saying "Yes":The current key is mapped to some value in JSON_YES.*)
(*                                                                     *)
(* Statement:                                                          *)
(* 1. It is Yes XOR No (see above definitions 2, 3).                   *)
(* 1.1.1. If you do not say anything, then it is No.                   *)
(* 1.1.2. If you say "emptyset" (None, NULL, "", …), then it is No.    *)
(* 1.1.3. If you say "No", then it is No.                              *)
(* 1.2.   If you say "Yes", then you do value of key right now.        *)
(* 4.   You do not neither do nor say anything else.                   *)
(*                                                                     *)
(* Implementation                                                      *)
(* The "yes or no" key Y_N                                             *)
(*    (see Statement 1 for existence, Statement 4 for uniqueness)      *)
(* is always the String "Y/N".                                         *)
(* Moreover, we expect you actually do something relevant/nontrivial   *)
(* This latter requirement cannot be implemented from a general case,  *)
(* since:                                                              *)
(* (a) "relevant" and "nontrivial" are context-dependent.              *)
(* (b) The context space is countable but infinite.                    *)
(* A complementary approach is about defining                          *)
(*     EXCLUDED_BY_YES_OR_NO_POLICY                                    *)
(* as the minimal set of what is either trivial or irrelevant.         *)
(* This set is not constructed ;) .                                    *)
(*    (In practice, EXCLUDED_BY_YES_OR_NO_POLICY should contain,       *)
(*     at least, boolean and numerical value                           *)
(* Hence, we cannot guarantee that the YesOrNo policy is implemented.  *)
(* But we can check that the policy is "followed", in the sense that:  *)
(* i. The policy is partially implemented and:                         *)
(* ii. If the provided content is actually relevant,                   *)
(*         then the policy is (nonprovably) implemented.               *)
(*                                                                     *)
(* Test / action'isFollowingYesOrNoPolicy(f)'                          *)
(* We expect the atom f to be a "first-degree subrecord" of preferences*)
(*     (documentclass|-> …, import_packages|-> …, and so on).          *)
(* isFollowingYesOrNoPolicy(f) is TRUE if.f f follows YesOrNo.         *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
isFollowingYesOrNoPolicy(f) == 
    /\ Y_N \in DOMAIN f                 \* the YesOrNo switch button
    /\ Cardinality(DOMAIN f) = 2        \* See Statement 4
    /\  \/     f[Y_N] \in JSON_NO       \* It is No
        \/  /\ f[Y_N] \in JSON_YES      \* It is Yes, and we "do well":
            /\ \A key \in (DOMAIN f)\{Y_N}: 
                /\ f[key] \in EXCLUDED_BY_YES_OR_NO_POLICY

(* YesOrNo policy: END ------------------------------------------------------*)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Either you want to implement YesOrNo (see above),                   *)
(* either you want to do something entirely different.                 *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
isCompatibleWithYesOrNoPolicy(f) == XOR(
    isFollowingYesOrNoPolicy(f),
    Y_N \notin DOMAIN f)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* isPreferencesFollowingSpec = TRUE if.f                              *)
(* preferences follow the specs.                                       *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
isPreferencesFollowingSpec ==
       \*
       \* First, only a specific range for the keys: 
    /\ DOMAIN preferences \subseteq DOMAIN_OF_PREFERENCES
       \* Next, every "subrecord" must be compatible with YesOrNo.
    /\ \A key \in DOMAIN preferences: 
          isCompatibleWithYesOrNoPolicy(preferences[key])

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Remark: If it is YesOrNo, then it is optional,                      *) 
(* since you cannot turn off a mandatory feature.                      *)
(* In other words, we have the following criterion:                    *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
isOptional(record) == 
    \* IF
    isFollowingYesOrNoPolicy(record)
    \* THEN TRUE ELSE FALSE

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Initial state                                                       *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
InitPreferences == 
    /\ preferences \in SET_OF_PREFERENCES

InitCorrectness == 
    /\ InitPreferences
       \*
       \* IF we do not believe that our current preferences file is legal,
       \* then, there is no process at all, we just go nack to work:
       \* Of course, up to now, nothing has been proved:
    /\ isPreferencesFileCompliant = TRUE 

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Next step                                                           *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
NextCorrectness == 
    /\ isPreferencesFollowingSpec
    /\ isPreferencesFileCompliant' = isPreferencesFollowingSpec
    /\ UNCHANGED preferences

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Invariants                                                          *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Properties                                                          *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
\* We can assume that our preferences comply with all policies:
\* Under the specs: 
\* [][isPreferencesFileCompliant]_<<
\*    isPreferencesFileCompliant
\*>>
\* Check with TLC must be OK. 
\* I consider it as an invariant, even if it's not syntactically true, 
\* since isPreferencesFileCompliantNAME variables are primed.


===============================================================================
