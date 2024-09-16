#
# italian scene rebuilder
# friol 2k24
#

import json;
import urllib.request;
from bs4 import BeautifulSoup;
import datetime;

outFile=None;

#

def getDemographicData(dzid,groupName):
    
    numTotalMembers=0;
    numItalianMembers=0;

    # https://demozoo.org/groups/11518/
    # scrape url

    url2scrape="https://demozoo.org/groups/"+dzid+"/";

    try:
        fp = urllib.request.urlopen(url2scrape);
        mybytes = fp.read();
        pageContent = mybytes.decode("utf8")
        fp.close();
    except:
        return 0,0;

    pageSoup = BeautifulSoup(pageContent,features="html.parser");
    members=pageSoup.find("ul", class_="memberships");
    for m in members:
        #outFile.write(m);
        if (str(m).find("li class=\"scener")!=-1):
            numTotalMembers+=1;
        if (str(m).find('it.png')>0):
            numItalianMembers+=1;

    try:
        outFile.write(groupName+","+url2scrape+","+str(numTotalMembers)+","+str(numItalianMembers));
    except:
        print("Unprintable group");

    return numTotalMembers,numItalianMembers;

def identifyItalianGroups():

    with open('pouetdatadump-groups-20240911.json', 'r') as file:
        jsonGroups = json.load(file);

    i=0;
    for group in jsonGroups["groups"]:
        demozooId=str(group["demozoo"]);
        if (demozooId!="0") and (demozooId!="None"):
            numComponents,italianComponents=getDemographicData(demozooId,group["name"]);
            i+=1;
    
    print("Total groups widh demozoo id: "+str(i));

def buildHTMLTable():

    current_time = datetime.datetime.now();
    outFile.write("<small>Creation timestamp:"+str(current_time)+"</small>");

    with open("iGroupz.txt") as file:
        lines = [line.rstrip() for line in file];

    outFile.write("<table>");
    outFile.write("<thead><tr><td>Demogroup</td><td>Productions</td></tr></thead>");

    linesCounter=0;
    while linesCounter<len(lines):
        l=lines[linesCounter];

        url2scrape=l;
        #print("Visiting "+url2scrape);

        try:
            fp = urllib.request.urlopen(url2scrape);
            mybytes = fp.read();
            pageContent = mybytes.decode("utf8")
            fp.close();
        except:
            print("Unable to reach url");

        pageSoup = BeautifulSoup(pageContent,features="html.parser");
        groupName=pageSoup.find("div", class_="focus_title group_name");
        if groupName==None:
            groupName=pageSoup.find("div", class_="focus_title scener_name");
        gName=str(groupName.find("h2")).replace("<h2>","").replace("</h2>","");
        #print(gName);

        #

        # ok, in HTML now

        outFile.write("<tr>");
        outFile.write("<td width=20%><a target=\"_blank\" href='"+url2scrape+"'>"+gName+"</a>");
        outFile.write("<td><table class=\"innerTable\">");

        prodsDiv=pageSoup.find('div', attrs={'id':'main_column'})
        table=prodsDiv.find('table');
        rows = table.find_all('tr')
        for row in rows:
            outFile.write("<tr>");
            cols = row.find_all('td');
            cols = [ele.text.strip() for ele in cols];

            colnum=0;
            for c in cols:
                if (colnum!=0) and (colnum!=2) and (c!=""):
                    if (colnum==1):
                        outFile.write("<td width=80%>");
                    else:
                        outFile.write("<td width=20%>");
                    if (colnum==1):
                        c="<b>"+c;
                        c=c.replace("\n\n\n","</b>");
                    outFile.write(c);
                    outFile.write("</td>");
                colnum+=1;
            outFile.write("</tr>");

        outFile.write("</table></td>");
        outFile.write("</tr>");
    
        linesCounter+=1;


    outFile.write("</table>");


def HTMLPrelude():

    with open("main.html") as file:
        lines = [line.rstrip() for line in file];

    for l in lines:
        outFile.write(l);

def HTMLClosure():
    outFile.write("<br/><small>(made by Friol with <3)</small><br/></body></html>");

#
#
#

#identifyItalianGroups();

print("Rebuilding the universe...");
outFile = open("index.html", "w");

HTMLPrelude();
buildHTMLTable();
HTMLClosure();

outFile.close();
print("Done!");
