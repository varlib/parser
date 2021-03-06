from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import csv
import argparse
import smtplib
import os


def start_parser(startline):
    n = 0
    with open('list.csv', newline='') as File:

        reader = csv.reader(File, delimiter=';', quotechar=',',
                            quoting=csv.QUOTE_ALL)
        fileend = 'end.csv'
        # if os.path.isfile(fileend):
        # os.remove(fileend)

        for row in reader:
            n += 1
            if n > startline:
                try:
                    url = row[1]
                except:
                    url = ''

                if 'volvo' not in url:
                    print('not url')
                else:
                    try:
                        page = requests.get(url)
                        if page.status_code != 200:
                            print('URL ERROR: ' + ' (' + row[0] + ')')
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
                    except:
                        sendMail("Server: 10.25.1.45 | Parser error in line: "+str(n))
                        start_parser(n)


def getParam():
    param = argparse.ArgumentParser()
    param.add_argument('position', nargs='?')
    return param

def sendMail(tSub):
    host = 'mail.mjr.local'
    subject = tSub
    to = 'LOG_IT_SUPPORT@mjr.local'
    From = 'noreply@mjr.local'
    text = tSub

    body = "\r\n".join((
        "From: %s" % From,
        "To: %s" % to,
        "Subject: %s" % subject,
        "",
        text
    ))
    server = smtplib.SMTP(host)
    server.sendmail(From, [to], body)
    server.quit()


if __name__ == '__main__':
    print('Start parser')
    param = getParam()
    namespace = param.parse_args()
    position = namespace.position

    start_time = datetime.now()
    if position:
        print('Position start ' + position)
        start_parser(int(position))
    else:
        print('Position start 0')
        start_parser(0)
    print(datetime.now() - start_time)
    sendMail('Parser completed processing')
