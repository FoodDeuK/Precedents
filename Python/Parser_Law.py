import pandas as pd
import xml.etree.ElementTree as ET
import sqlite3

from urllib.request import urlopen
from tqdm import trange

conn = sqlite3.connect("Laws.db")
curs = conn.cursor()

url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=law&type=XML"
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
            법령일련번호 = node.find('법령일련번호').text
            현행연혁코드 = node.find('현행연혁코드').text
            법령명한글 = node.find('법령명한글').text
            법령약칭명 = node.find('법령약칭명').text
            법령ID = node.find('법령ID').text
            공포일자 = node.find('공포일자').text
            공포번호 = node.find('공포번호').text
            제개정구분명 = node.find('제개정구분명').text
            소관부처코드 = node.find('소관부처코드').text
            소관부처명 = node.find('소관부처명').text
            법령구분명 = node.find('법령구분명').text
            소관부처명 = node.find('소관부처명').text
            시행일자 = node.find('시행일자').text
            자법타법여부 = node.find('자법타법여부').text
            법령상세링크 = node.find('법령상세링크').text

            rows.append({'법령일련번호': 법령일련번호, '현행연혁코드': 현행연혁코드, '법령명한글': 법령명한글, '법령약칭명': 법령약칭명, '법령ID': 법령ID,
                        '공포일자': 공포일자, '공포번호': 공포번호, '제개정구분명': 제개정구분명, '소관부처코드': 소관부처코드, '소관부처명': 소관부처명,
                        '소관부처코드': 소관부처코드, '법령구분명': 법령구분명, '시행일자': 시행일자, '자법타법여부': 자법타법여부, '법령상세링크': 법령상세링크})
            
        except Exception as e:
            continue
    
    pages += 1
    url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=law&type=XML&page={}".format(pages)
    response = urlopen(url).read()
    xtree = ET.fromstring(response)
cases = pd.DataFrame(rows)
cases.to_sql('Laws', conn, index = False)