----------------------- MODULE Md2LaTeXSpecifications -----------------------
EXTENDS Md2LaTeXAlgorithms

Init == InitAlgorithms

Next == NextAlgorithms


Spec == Init /\ [][NextAlgorithms]_<<
    entityState, 
    preferences, 
    isPreferencesFileCompliant,
    preferences_as_dict>>

=============================================================================
