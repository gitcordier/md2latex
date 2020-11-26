import_from="/Users/gcordier/.tlaplus/Md2LaTeXSpecifications/"
import_from="/Users/gcordier/.tlaplus/Md2LaTeXSpecifications/"

tex_file_=( Md2LaTeXCorrectness 
Md2LaTeXSystemDesign 
Md2LaTeXAlgorithms 
Md2LaTeXSpecifications 
Md2LaTexSystemDesignPreferencesFile )

for e in "${tex_file_[@]}"
do 
cp $import_from"Md2LaTeXSpecifications.toolbox/"$e".tex" $e".tex"
cp $import_from$e".tla" "../tla/"$e".tla"
done

base="md2latex"
name=$base".specifications"
#
python3 cut.py
#

xelatex $name".md.tex"
mv $name".md.pdf" "../pdf/"$name".md.pdf"
