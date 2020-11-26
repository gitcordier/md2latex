------------------------- MODULE Md2LaTeXAlgorithms ---------------------------
EXTENDS Md2LaTeXSystemDesign, Functions

(* At run time / compile time, the preferences file is parsed,         *)
(* which yields a dictionary (in Python) / HashMap (in Java) object,   *)
(* namely 'preferences_as_dict'.                                       *)
(* We specify the parsing process.                                     *)
VARIABLE preferences_as_dict

\* So that preference_[key] is the actual setting 'key': 
preference_ == [ key \in DOMAIN preferences |-> preferences[key]]

(*                                                                     *)
(* If it is No, then no setting.                                       *)
(* So, current key is off preferences_as_dict.                         *)
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
    /\ preferences_as_dict = preferences

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Next state                                                          *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
NextAlgorithms == 
    /\ NextSystemDesign
    /\ preferences_as_dict' = parsing

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Invariant                                                           *)
(* IsParsingOK = TRUE if.f the parsing outputs a dictionary that:      *)
(* i. is compatible with the YesOrNo policy, i.e every subrecord is so;*)
(* ii.is 'lean', in the sense that no "turned off" option              *)
(* - see Md2LaTeXSystemDesign - keeps existing in the dictionary       *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* This is actually repeating what is done with Md2LaTeXSystemDesign,  *)
(* but this time, it is an invariant!                                  *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
IsParsingOK == 
    \/ InitAlgorithms
    \/  \A key \in DOMAIN preferences_as_dict:
            /\ isCompatibleWithYesOrNoPolicy(preference_[key])
            /\  XOR(\* either:
                    /\ ~isFollowingYesOrNoPolicy(preference_[key]),
                    \* either:
                    /\ isFollowingYesOrNoPolicy(preference_[key])
                    /\ preferences_as_dict[key][Y_N] \in JSON_YES)
 
===============================================================================

