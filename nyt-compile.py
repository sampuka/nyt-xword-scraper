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

with open('template.tex', 'r') as file:
    filedata = file.read()

filedata = filedata.replace('$TITLE$', data.title)
filedata = filedata.replace('$AUTHOR$', data.author)
filedata = filedata.replace('$EDITOR$', data.editor)

gridtxt = ""

for row in data.grid:
    for col in row:
        gridtxt += "|"
        if col[0] == '#':
            gridtxt += "*    "
        elif col[1] != '':
            gridtxt += "["+str(col[1])+"]" + str(col[0])
        else:
            gridtxt += str(col[0]) + "    "

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

acrosstxt = acrosstxt.replace('_','\_')
downtxt = downtxt.replace('_','\_')

acrosstxt = acrosstxt.replace('%','\%')
downtxt = downtxt.replace('%','\%')

filedata = filedata.replace('$ACROSS$', acrosstxt)
filedata = filedata.replace('$DOWN$', downtxt)

with open('tocompile.tex', 'w') as file:
    file.write(filedata)

os.system("pdflatex tocompile.tex && mv tocompile.pdf " + "done.pdf" + " && rm tocompile.*")
