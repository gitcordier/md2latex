------------------------ MODULE Md2LaTeXCorrectnessPreferencesFile -----------
EXTENDS Md2LaTeXCorrectness, FiniteSets

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* The preferences are identified with a file NAME.preferences.json    *)
(*                                                                     *)
(* isPreferencesFileCompliant keeps track of preferences compliance.   *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
VARIABLES preferences, isPreferencesFileCompliant

(* Convenient operators *)
XOR(a, b) == (a \/ b) /\ (~b \/ ~a)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* The YesOrNo policy (2nd part):                                      *)
(* Test/action isFollowingYesOrNoPolicy(f):                            *)
(*     Definition:                                                     *)
(*         isFollowingYesOrNoPolicy(f) is TRUE if.f f follows YesOrNo. *)
(*                                                                     *)
(* We expect the atom f to be a "first-degree subrecord" of preferences*)
(*     (e.g. documentclass|-> …, import_packages|->…).                 *)
(* Conversely, preferences record is flat                              *)
(*     (see SET_OF_PREFERENCES definition).                            *)
(* No recursive check, then.                                           *)
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
isFollowingYesOrNoPolicy(f) == 
    IF Y_N \in DOMAIN f                   \* the YesOrNo switch button
    THEN 
        /\ Cardinality(DOMAIN f) = 2      \* See Statement 2
        /\ XOR(f[Y_N] \in JSON_NO,        \* It is No
            /\ f[Y_N] \in JSON_YES        \* It is Yes, and we "do well":
            /\ \A key \in (DOMAIN f)\{Y_N}: 
                f[key] \notin EXCLUDED_BY_YES_OR_NO_POLICY)
    ELSE FALSE

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
    \* THEN TRUE 
    \* ELSE FALSE

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* The isOptional term is clearly misleading… there is no contradiction*)
(* with the fact that all keys are nonoptional. The isOptional operator*)
(* is about the features themselves. TODO: (!) Make that clear.        *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
(* Initial state                                                       *) 
(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)
InitPreferences == 
    /\ preferences \in SET_OF_PREFERENCES

InitCorrectness == 
    /\ InitPreferences
       \*
       \* IF we do not believe that our current preferences file is legal,
       \* then, there is no process at all, we just go back to work:
       \* Of course, up to now, nothing has been proved:
    /\ isPreferencesFileCompliant = TRUE \* Conjecture

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



===============================================================================
