from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import csv
import os

start_time = datetime.now()
n = 0
with open('list.csv', newline='') as File:

    reader = csv.reader(File, delimiter=';', quotechar=',',
                            quoting=csv.QUOTE_ALL)
    fileend = 'end.csv'
    #if os.path.isfile(fileend):
        #os.remove(fileend)

    for row in reader:
        n += 1
        if n > 44778:
            try:
                url = row[1]
            except:
                url = ''

            if 'volvo' not in url:
                print('not url')
            else:
                page = requests.get(url)
                if page.status_code != 200:
                    print('URL ERROR: ' + page.status + ' ('+row[0]+')')
                else:
                    soup = BeautifulSoup(page.text, "html.parser")
                    ostat = soup.find('div', class_='product-table__qty')
                    if ostat:
                        ostat = ostat.text
                        ostat = re.findall('(\d+)', ostat)
                        if not ostat:
                            print('под заказ')
                        else:
                            ostat = [row[0], ostat[0]]
                            print(ostat)
                            with open(fileend, 'a', newline='') as filecsv:
                                writer = csv.writer(filecsv, quoting=csv.QUOTE_ALL)
                                writer.writerow(ostat)
                    else:
                        print('error find class')

print(datetime.now() - start_time)