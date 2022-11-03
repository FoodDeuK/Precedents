import pandas as pd
import xml.etree.ElementTree as ET
import sqlite3

from urllib.request import urlopen
from tqdm import trange
import re
import os

conn_fetcher = sqlite3.connect("Precedents.db")
curs_fetcher = conn_fetcher.cursor()

sql = "select * from Precedents"
curs_fetcher.execute(sql)

fetchedData = curs_fetcher.fetchall()
totalCnt = len(fetchedData)
fetchedData = [list(fetchedData[x]) for x in range(totalCnt)]

contents = ['판시사항', '판결요지', '참조조문', '참조판례', '판례내용']

def remove_tag(content):
    cleaned_text = re.sub('<.*?>', '', content)
    return cleaned_text

for content in contents:
    os.makedirs('./Cases/{}'.format(content), exist_ok = True)

for i in trange(totalCnt-61669):                                        # 판례내용 미존재로 인해 판례번호 228659번 제외
    url = "https://www.law.go.kr"
    link = fetchedData[i+61669][9].replace('HTML', 'XML')
    url += link
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

    for content in contents:
        try:
            text = xtree.find(content).text
            if text is None:
                text = '내용없음'
            else:
                text = remove_tag(text)
        except:
            file = './Error.txt'
            with open(file, 'w+') as err:
                err.write(fetchedData[i][0])
                err.close()
        
        file = './Cases/' + content + '/' + xtree.find('판례정보일련번호').text + '.txt'
        with open(file, 'w') as c:
            c.write(text)
            c.close()