import datetime
import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class XWData:
    date = datetime.datetime(2000, 1, 1)
    url = "Default URL"
    title = "Default Title"
    author = "Default Author"
    editor = "Default Editor"
    keyclue = "Default KeyClue"

    grid = []
    across = []
    down = []

    def __str__(self):
        return "Title = " + str(self.title) + "\nauthor = " + self.author + "\neditor = " + self.editor + "\nkeyclue = " + self.keyclue


def xwordinfo_scraper(date):
    url = "http://www.xwordinfo.com/Crossword?date="+str(date.month)+"/"+str(date.day)+"/"+str(date.year)
    html = requests.get(url).text
    soup = BeautifulSoup(html,features="html.parser")

    data = XWData()
    data.date = date
    data.url = url
    data.title = str(soup.find(id="PuzTitle").string)
    data.keyclue = str(soup.find(id="CPHContent_KeyClue").string)

    aegrid = soup.find(id="CPHContent_AEGrid")
    data.author = str(aegrid.contents[2].string)
    data.editor = str(aegrid.contents[5].string)

    gridtable = soup.find(id="PuzTable").contents[1:-1]
    for r in range(0,len(gridtable)):
        data.grid.append([])
        row = gridtable[r].contents[0:-1]

        for c in range(1,len(row)):
            cell = row[c].contents
            if len(cell) == 0:
                data.grid[r].append(['#', ''])
            elif len(cell) == 2:
                if str(cell[0].string) == "None":
                    data.grid[r].append([str(cell[1].string), ''])
                else:
                    data.grid[r].append([str(cell[1].string), cell[0].string])

    cluebox = soup.find(id="CPHContent_ClueBox").contents
    acluebox = cluebox[1]
    dcluebox = cluebox[3]
    aclues = acluebox.contents[3].contents
    dclues = dcluebox.contents[3].contents

    for c in range(0,len(aclues)//2):
        cluenum = str(aclues[c*2].string)
        cluetxt = aclues[c*2+1].contents[0][:-3]
        clueans = str(aclues[c*2+1].contents[1].string)
        data.across.append([cluenum, cluetxt, clueans])
        #print(cluenum + ": " + cluetxt)

    for c in range(0,len(dclues)//2):
        cluenum = str(dclues[c*2].string)
        cluetxt = dclues[c*2+1].contents[0][:-3]
        clueans = str(dclues[c*2+1].contents[1].string)
        data.down.append([cluenum, cluetxt, clueans])
        #print(cluenum + ": " + cluetxt)

    return data

if __name__ == "__main__":
    yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
    data = xwordinfo_scraper(yesterday)

    print(data.url)
    print(data)
    print(data.grid)
    print(data.across)
    print(data.down)
