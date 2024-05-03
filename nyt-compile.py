from xwordinfo_scraper import *

import sys
import os
import datetime
import fileinput

if len(sys.argv) != 4:
    print("Usage: python3 " + sys.argv[0] + " YYYY MM DD")
    sys.exit()

date = datetime.datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

data = xwordinfo_scraper(date)

template_file = 'template.tex'

if date.weekday() == 6:
    template_file = 'template-sunday.tex'

with open(template_file, 'r') as file:
    filedata = file.read()

filedata = filedata.replace('$TITLE$', data.title)
filedata = filedata.replace('$AUTHOR$', data.author)
filedata = filedata.replace('$EDITOR$', data.editor)

gridtxt = ""

for row in data.grid:
    for col in row:
        gridtxt += "|[" + col[2] + "][" + col[0] + "]" + col[1]

    gridtxt += "|.\n"

filedata = filedata.replace('$WIDTH$', str(len(data.grid[0])))
filedata = filedata.replace('$HEIGHT$', str(len(data.grid)))
filedata = filedata.replace('$GRID$', gridtxt)

acrosstxt = ""
downtxt = ""

for clue in data.across:
    acrosstxt += "\\Clue{\\textbf{" + clue[0] + "}}{" + clue[2] + "}{" + clue[1] + "} \\\\\n"

for clue in data.down:
    downtxt += "\\Clue{\\textbf{" + clue[0] + "}}{" + clue[2] + "}{" + clue[1] + "} \\\\\n"

replace_list = [('_','\_'), ('%','\%'), ('$','\$'), ('#','\#'), ('&','\&'), ('∼','\\texttildelow'), ('^','\\textasciicircum'), ('Ω','$\Omega$')]

for (a,b) in replace_list:
    acrosstxt = acrosstxt.replace(a,b)
    downtxt = downtxt.replace(a,b)

filedata = filedata.replace('$ACROSS$', acrosstxt)
filedata = filedata.replace('$DOWN$', downtxt)

with open('tocompile.tex', 'w') as file:
    file.write(filedata)

filename = "NYT_Crossword_" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".pdf"
#os.system("pdflatex tocompile.tex && mv tocompile.pdf " + filename)
os.system("pdflatex tocompile.tex && mv tocompile.pdf " + filename + " && rm tocompile.*")
