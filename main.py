from bs4 import BeautifulSoup
import requests
import re
import csv
import os

with open('list.csv', newline='') as File:
    reader = csv.reader(File, delimiter=';', quotechar=',',
                        quoting=csv.QUOTE_ALL)
    fileend = 'end.csv'
    if os.path.isfile(fileend):
        os.remove('end.csv')

    for row in reader:
        url = row[1]
        if 'volvo' not in url:
            print('URL: ' + url)
        else:
            page = requests.get(url)

            soup = BeautifulSoup(page.text, "html.parser")

            ostat = soup.find('div', class_='product-table__qty')

            try:
                ostat = ostat.text
                ostat = re.findall('(\d+)', ostat)

                ostat = [row[0], ostat[0]]

                if not ostat:
                    print('под заказ')
                else:
                    print(ostat)
                    with open(fileend, 'a', newline='') as filecsv:
                        writer = csv.writer(filecsv, quoting=csv.QUOTE_ALL)
                        writer.writerow(ostat)
            except:
                print('ERROR: '+row[0])