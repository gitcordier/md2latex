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

(*                                                                     *)
(* Initial state                                                       *)
(*                                                                     *)
InitAlgorithms == 
    /\ InitSystemDesign
    /\ preferences_as_dict = preferences

(*                                                                     *)
(* Next state                                                          *)
(*                                                                     *)
NextAlgorithms == 
    /\  NextSystemDesign
    /\ preferences_as_dict' = parsing
 

===============================================================================

