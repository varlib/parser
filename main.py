from bs4 import BeautifulSoup
import requests
import re
import csv

with open('list.csv', newline='') as File:
    reader = csv.reader(File, delimiter=';', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        #print(row[1])
        #url = 'https://volvogroupshop.ru/parts/section/346947/part/548241/?case=detail&part_number=VO20535535'
        url = row[1]
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")

        ostat = soup.find('div', class_='product-table__qty')

        ostat = ostat.text
        ostat = re.findall('(\d+)', ostat)


        if not ostat:
            print('под заказ')
        else:
            print(ostat)
            with open('end.csv', 'a', newline='') as filecsv:
                writer = csv.writer(filecsv, quoting=csv.QUOTE_ALL)
                writer.writerow(map(int, ostat))