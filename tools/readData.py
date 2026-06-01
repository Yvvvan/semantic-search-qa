import csv


cnt=0
"""
with open('./data/hansche-qa-arbeitsrecht.csv', encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';', )
        next(readCSV, None)  # skip the headers
        for row in readCSV:
                # keep count of # rows processed
                cnt += 1
                #print(cnt)

print(cnt,len(row))
"""

with open('./data/hansche-qa-arbeitsrecht.csv', encoding="utf8") as csvfile, open('./data/hansche-qa-arbeitsrecht-id.csv', 'w') as output:
        readCSV = csv.reader(csvfile, delimiter=';', )
        writer = csv.writer(output, delimiter = ';' )
        all = []
        row = next(readCSV)
        row.insert(0,'id')
        all.append(row)
        count=0
        for row in readCSV:
                count+=1
                row.insert(0, count)
                all.append(row)
                # keep count of # rows processed
                cnt += 1
                #print(cnt)
        writer.writerows(all)

print(cnt,len(row))
