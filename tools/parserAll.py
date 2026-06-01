"""Project maintainers, 2021."""

from pyquery import PyQuery
import requests
import re
r = requests.get('https://www.hensche.de/Rechtsanwalt_Arbeitsrecht_Handbuch.html')
html=r.text

pq = PyQuery(html)
tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(6)')
hrefs = re.findall(r"(?<=href=\")(.*)(?=\"\sx)", str(tag),re.IGNORECASE)
for h in hrefs:
    print('https://www.hensche.de'+h.split('\"')[0])

with open('outputallv2.txt', 'w') as filehandle:
    for href in hrefs:
        url = 'https://www.hensche.de'+href.split('\"')[0]

        r = requests.get(url)
        html=r.text
        pq = PyQuery(html)

        tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(4) > ul.toc') # or     tag = pq('div.class')
        qs=tag.text().split('\n')
        if not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(5) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(6) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(7) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(8) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(9) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(10) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(4) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')
        elif not qs[0]:
            tag = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy > div:nth-child(4) > ul.toc') # or     tag = pq('div.class')
            qs=tag.text().split('\n')


        if qs[0]:
            print('unterseite hrefs ',qs[0], qs[1], qs[len(qs)-1])

            spliter = ''
            for q in qs:
                if q != qs[len(qs)-1]:
                    spliter+=q+'|'
                else:
                    spliter+=q
            #print(spliter, '\n','*********************','\n')

            tag_body = pq('body > div.mainwrapper > div.contentwrapper > div.rechte_spalte > div.maincontent > div.copy')
            body=tag_body.text().split(qs[len(qs)-1], 1)[1]
            print (body)


            segments_ = re.split(spliter, body)
            i=0
            j=0
            segments = [s for s in segments_ if s and len(s) > 10]
            print(len(qs),len(segments),len(segments_))

            for i in range(len(qs)): 
                if j in range(len(segments)):
                    print(i,qs[i],':',j,segments[j])
                    filehandle.write(url +'#+#'+ qs[i] +'#+#'+ segments[j]+'\n')
                    i+=1
                    j+=1
