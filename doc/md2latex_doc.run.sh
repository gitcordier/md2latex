bin="xelatex"
name="md2latex_doc"
launch_pdf_reader="open -a skim ${var}.pdf"
launch_md2latex="../md2latex/launch_md2latex.py"
path="src/"
dst="dst/"
python3 "${launch_md2latex}" "${path}" "${name}.md"  "${name}.preferences.json"

#mv "${path}${name}.md.tex" "${dst}${name}.md.tex"
#mv "${path}${name}.md.conversion.log" "${dst}${name}.md.conversion.log"
#cd "${dst}"
#${bin} "${name}.md.tex" 
#${bin} "${name}.md.tex"
#${launch_pdf_reader}
