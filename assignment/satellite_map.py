import requests
from bs4 import BeautifulSoup
from draw import *

# 发送HTTP请求获取网页内容
url = "https://satellitemap.space/satellites.html"  
response = requests.get(url)

# 解析HTML网页
soup = BeautifulSoup(response.text, 'html.parser')

# 找到表格
table = soup.find('table', {'class': 'table table-dark table-sm'})

# 找到"Alt (km)"和"Name"这两列的索引
headers = table.find('tr').find_all('th')
alt_index = 0
name_index = 0
for i, header in enumerate(headers):
    if header.text.strip() == 'Alt (km)':
        alt_index = i
    elif header.text.strip() == 'Norad':
        norad_index = i

# 提取数据
data = []
rows = table.find_all('tr')[1:]  
for row in rows:
    cols = row.find_all('td')
    if len(cols) > max(alt_index, norad_index):
        alt_value = cols[alt_index].text.strip()
        norad_value = cols[norad_index].text.strip()  
        data.append((alt_value, norad_value))

# 打印数据
for i, (alt, name) in enumerate(data):
    print(f"Alt (km):{alt}")
    print(f"Norad:{name}")
    print()

# 进行数字可视化
norads = [int(item[1]) for item in data]
alts = []
for item in data:
    if item[0] != '':
        alts.append(float(item[0]))
    else:
        alts.append(0)
draw_scatter2(norads, alts)