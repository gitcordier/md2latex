------------------------- MODULE Md2LaTeXAlgorithms ---------------------------
EXTENDS Md2LaTeXSystemDesign, Functions

(* At run time / compile time, the preferences file is parsed,         *)
(* which yields a dictionary 'choice_'.                                *)
(* We below specify the parsing process.                               *)
VARIABLE choice_
(*                                                                     *)
(* If it is No, then no setting.                                       *)
(* So, current key is not part of choice_.                             *)
(*                                                                     *)
\* First, filter:
relevantKeys == {
    key \in DOMAIN preferences:
        \/  key = "documentclass" 
        \/  /\ isFollowingYesOrNoPolicy(preferences[key])  
            /\ preferences[key][Y_N] \notin JSON_NO
}

\* Next, stir up:
parsing == [key \in relevantKeys |-> preferences[key]]

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Initial state                                                       *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
InitAlgorithms == 
    /\ InitSystemDesign
    /\ choice_ = preferences

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Next state                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
NextAlgorithms == 
    /\ NextSystemDesign
    /\ choice_' = parsing

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Invariant                                                           *)
(* IsParsingOK = TRUE if.f the parsing outputs a dictionary that:      *)
(* i. is compatible with the YesOrNo policy, i.e every subrecord is so;*)
(* ii.is 'lean', in the sense that no "turned off" option              *)
(*      - see Md2LaTeXSystemDesign - keeps existing in the dictionary; *) 
(* iii. has no extra key, i.e. all key come from DOMAIN_OF_PREFERENCES *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

IsParsingOK == 
    \/ InitAlgorithms
    \/  \A key \in DOMAIN choice_:
            /\ isCompatibleWithYesOrNoPolicy(preferences[key])
            /\  XOR(\* either:
                    /\ ~isFollowingYesOrNoPolicy(preferences[key]),
                    \* either:
                    /\ isFollowingYesOrNoPolicy(preferences[key])
                    /\ choice_[key][Y_N] \in JSON_YES)
 
\* It means some redundant boolean tests, but we do not care about, since
\* we are are not aiming at optimal predicate computation, only specifications!

===============================================================================

