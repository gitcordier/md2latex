----------------------- MODULE Md2LaTeXSpecifications -----------------------
EXTENDS Md2LaTeXAlgorithms

Init == InitAlgorithms

Next == NextAlgorithms


Spec == Init /\ [][NextAlgorithms]_<<
    preferences, 
    isPreferencesFileCompliant,
    choice_>>

=============================================================================
