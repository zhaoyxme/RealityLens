import re

import openpyxl
import requests
from lxml import etree
from bs4 import BeautifulSoup
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}
workbook = openpyxl.load_workbook('excel.xlsx')
sheet = workbook['Sheet1']
a = 'A{}'
b = 'B{}'
c = 'C{}'
d = 'D{}'
datas = []
for cell in sheet['A']:
    datas.append(cell.value)

# print(datas)
# print(datas[0].strip())
# for i in range(0,len(datas)-1):
#     data = datas[i].strip()
#     print(data)
res = requests.get('https://news-view.webflow.io/',headers=headers)
# print(res)
# print(res.text)
html = etree.HTML(res.text)

detail_urls = re.findall('<a data-w-id=".*?".*?href="(.*?)".*?class=".*?w-inline-block">',res.text,re.S)
# print(detail_urls)
print(len(detail_urls))
fina_content_list = []
for detail_url in detail_urls:
    detail_url = 'https://news-view.webflow.io' + detail_url
    response = requests.get(detail_url,headers=headers)
    print(detail_url)
    # print(response.text)
    soup = BeautifulSoup(response.text,'lxml')
    # html = etree.HTML(response.text)
    contents = soup.select('div.main-news-details')[0]
    content = '\n'.join(list(contents.stripped_strings))
    # print(content)
    comments = soup.select('p.a-paragraph-regular')
    comment_list = []
    for comment in comments:
        comment = ','.join(list(comment.stripped_strings)).strip().replace('â','')
        comment_list.append(comment)
    # print(comments)
    fina_comment = '\n'.join(comment_list)
    # print(fina_comment)
    fina_content = content + '\n' + fina_comment
    # print(fina_content)
    fina_content_list.append(fina_content)
    # print(len(comment_list))

nn=1
finall = '\n'.join(fina_content_list)
print(finall)
for i in range(0,len(datas)):
    data = datas[i].strip()
    number = finall.count(data)
    sheet[c.format(nn)] = number
    nn+=1
    workbook.save('excel.xlsx')

workbook.close()