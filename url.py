import requests
import json
import csv



with open('temp_url.csv', newline='') as File:
    reader = csv.reader(File, delimiter=';', quotechar=',',
                            quoting=csv.QUOTE_ALL)
    fileend = 'url.csv'
    
    for row in reader:
        r = requests.post('https://volvogroupshop.ru/api/web/form/search/', json={"vinNumber": "", "chassisNumber":"", "detailNumber":row[2], "detailName":"", "model":""})
        data = r.json()["data"]
        url = [row[1], row[2], data["redirectUrl"]]
        with open(fileend, 'a', newline='') as filecsv:
            writer = csv.writer(filecsv, quoting=csv.QUOTE_ALL)
            writer.writerow(url)