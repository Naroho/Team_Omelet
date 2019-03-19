import requests
from bs4 import BeautifulSoup
import sys
import io

#남엽 work
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

code = '005930'
URL = "https://finance.naver.com/item/main.nhn?code={code}".format(code=code)

samsung_electronic = requests.get(URL)
html = samsung_electronic.text

soup = BeautifulSoup(html, 'html.parser')

finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]

th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
annual_date = th_data[3:7]
quarter_date = th_data[7:13]

finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
finance_data = [item.get_text().strip() for item in finance_html.select('td')]

import numpy as np

finance_data = np.array(finance_data)
finance_data.resize(len(finance_index), 10)

finance_date = annual_date + quarter_date

import pandas as pd
finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)

annual_finance = finance.iloc[:, :4]
quarter_finance = finance.iloc[:, 4:]

print(annual_finance)
print(quarter_finance)
