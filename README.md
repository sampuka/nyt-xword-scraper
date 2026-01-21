# nyt-xword-scraper

Scrapes XWordInfo and compiles printable pdfs. Very legal.

# Dependencies

sudo apt install python3 python3-venv python3-pip texlive texlive-latex-extra

# Usage

python3 -m venv .venv  
. .venv/bin/activate  
pip install -e .
nytcompile 2026 01 19
