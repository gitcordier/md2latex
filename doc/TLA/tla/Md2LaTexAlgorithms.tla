------------------------- MODULE Md2LaTeXAlgorithms ---------------------------
EXTENDS Md2LaTeXSystemDesign, Functions

(* At run time / compile time, the preferences file is parsed,         *)
(* which yields a dictionary (in Python) / HashMap (in Java) object,   *)
(* namely 'preferences_as_dict'.                                       *)
(* We specify the parsing process.                                     *)
VARIABLE preferences_as_dict

(*                                                                     *)
(* If it is No, then no setting.                                       *)
(* So, current key is off preferences_as_dict.                         *)
(*                                                                     *)
\* First, filter:
filteredKeys == {
    key \in DOMAIN preferences: 
        /\ isFollowingYesOrNoPolicy(preferences[key])  
        /\ preferences[key][Y_N] \notin JSON_NO
}

\* Next, stir up:
parsing == [key \in filteredKeys |-> preferences[key]]

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
            /\ isFollowingYesOrNoPolicy(preferences_as_dict[key])
            /\  XOR(\* either:
                    /\ ~isFollowingYesOrNoPolicy(preferences_as_dict[key])
                    /\ isCompatibleWithYesOrNoPolicy(preferences_as_dict[key]),
                    \* either:
                    /\ isFollowingYesOrNoPolicy(preferences_as_dict[key])
                    /\ preferences_as_dict[key][Y_N] \in JSON_YES)
 
===============================================================================

