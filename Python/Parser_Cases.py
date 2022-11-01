import pandas as pd
import xml.etree.ElementTree as ET
import sqlite3

from urllib.request import urlopen
from tqdm import trange

conn = sqlite3.connect("Precedents.db")
curs = conn.cursor()

url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=prec&type=XML"
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
        판례일련번호 = node.find('판례일련번호').text
        사건명 = node.find('사건명').text
        사건번호 = node.find('사건번호').text
        선고일자 = node.find('선고일자').text
        법원명 = node.find('법원명').text
        사건종류명 = node.find('사건종류명').text
        사건종류코드 = node.find('사건종류코드').text
        판결유형 = node.find('판결유형').text
        선고 = node.find('선고').text
        판례상세링크 = node.find('판례상세링크').text
    
        rows.append({'판례일련번호': 판례일련번호, '사건명': 사건명, '사건번호': 사건번호, '선고일자': 선고일자, '법원명': 법원명, '사건종류명': 사건종류명,
                    '사건종류코드': 사건종류코드, '판결유형': 판결유형, '선고': 선고, '판례상세링크': 판례상세링크})
    
    pages += 1
    url = "https://www.law.go.kr/DRF/lawSearch.do?OC=abs0lutezer0&target=prec&type=XML&page={}".format(pages)
    response = urlopen(url).read()
    xtree = ET.fromstring(response)
cases = pd.DataFrame(rows)
cases.to_sql('Precedents', conn, index = False)