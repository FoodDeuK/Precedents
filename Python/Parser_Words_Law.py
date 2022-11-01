import pandas as pd
import xml.etree.ElementTree as ET
import sqlite3

from urllib.request import urlopen
from tqdm import trange

conn = sqlite3.connect("Words_Law.db")
curs = conn.cursor()

url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=lstrm&type=XML"
response = urlopen(url).read()
xtree = ET.fromstring(response)

totalCnt = int(xtree.find('totalCnt').text)

pages = 1
rows = []
for x in trange(int(totalCnt / 20)):
    try:
        items = xtree[5:]
    except:
        break
    
    for node in items:
        try:
            법령용어ID = node.find('법령용어ID').text
            법령용어명 = node.find('법령용어명').text

            rows.append({'법령용어ID': 법령용어ID, '법령용어명': 법령용어명})
            
        except Exception as e:
            continue
    
    pages += 1
    url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=lstrm&type=XML&page={}".format(pages)
    response = urlopen(url).read()
    xtree = ET.fromstring(response)
cases = pd.DataFrame(rows)
cases.to_sql('Words_Law', conn, index = False)