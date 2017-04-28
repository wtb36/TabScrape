import DryscrapeUse
import dryscrape
import re
import csv
import sys

trys = 1
rematch = None

# Download page. Up to 4 trials.
while rematch is None:
    session = DryscrapeUse.wrapDryscrape(u'https://vlab.stern.nyu.edu/analysis/RISK.WORLDFIN-MR.GMES')
    code = session.grepCode('')
    rematch = re.search(u'href="#risk-graph">\\s*(.*)</table>', code)
    if (trys > 4):
        print('Seite konnte nicht geladen werden.')
        sys.exit()

# Write code to file.
with open('QuellCode.html','w') as output:
    output.write(code)

lines = rematch.group(1).split('href="#risk-graph">')
sriskP = []
rnk = []
sriskM = []
lrmes = []
beta = []
cor = []
vol = []
lvg = []

n = len(lines)

#infopattern= u'\\s*([0-9.]+.[0-9.]*)</td>'
infopattern = u'\\s*(.*)</td>'
for line in lines:
    informations = line.split('"value">')
    sriskP.append(re.search(infopattern, informations[1]).group(1))
    rnk.append(re.search(infopattern, informations[2]).group(1))
    sriskM.append(re.search(infopattern,informations[3]).group(1))
    lrmes.append(re.search(infopattern, informations[4]).group(1))
    beta.append(re.search(infopattern,informations[5]).group(1))
    cor.append(re.search(infopattern,informations[6]).group(1))
    vol.append(re.search(infopattern,informations[7]).group(1))
    lvg.append(re.search(infopattern,informations[8]).group(1))

names = [(re.search(u'\\s*(.*)</a></td>', le).group(1).split('</a>')[0]) for le in lines]

if rematch is not None:
    with open('FilterQuell.txt','w') as output:
        for i in range(0,n):
            output.write(lines[i])
            output.write('\n')

with open('names.txt','w') as output:
    for i in range(0,n):
        output.write(names[i])
        output.write('\n')

with open('data.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ";")
    writer.writerow(('Institution','SRISK%','RNK','SRISK ($ m)','LRMES','Beta','Cor','Vol','Lvg'))
    for i in range(0,n):
        writer.writerow((names[i],sriskP[i],rnk[i],sriskM[i],lrmes[i],beta[i],cor[i],vol[i],lvg[i]))
