------------------------ MODULE Md2LaTeXCorrectness ------------------------
(* For now we only aim at checking the correctness of the JSON Prefs*)
(* entities are: user (singleton), the JSONFile, the checker*)

VARIABLE entityState

(* To be expressive:*)
XOR(a, b) == (a \/ b) /\ (~a \/ ~b)

SetOfEntityStates == [
        user:{"working", "done"},
        prefs:{"not checked", "checked"} \times {"compliant", "not compliant"},
        checker:{"working", "done"}]   
                                    
InitCorrectness == 
    /\ entityState \in SetOfEntityStates
 
NextCorrectness == 
  (* checker is working:
    checker simply achieves processing. *)
        /\ entityState.checker = "working"
        /\ entityState' = [entityState EXCEPT !.checker = "done"]
  (*  checker is done:
   1. user is working:
      user achieves all current tasks *)
    \/  /\ entityState.user = "working" 
        /\ entityState.checker = "done"
        /\ entityState' = [entityState EXCEPT !.user = "done"]
    (* checker is done:
     2. user is done, checker is done: user goes back to work*)
    \/  /\ entityState.user = "done" 
        /\ entityState.checker = "done"
        /\ entityState' = [entityState EXCEPT !.user = "working"]

isDone == /\ entityState.user = "done" 
        /\ entityState.checker = "done"
    
=============================================================================
