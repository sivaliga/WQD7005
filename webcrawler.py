##########################################################################################

# Web crawling the real time data by using Python  (WQD7004 Programming for Data Science)
# Sivanesan Pillai (WQD170074)
# Mathavan Chandrasegaram (WQD170075)

##########################################################################################

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import csv
from pathlib import Path

csvExist = Path('petrolprice.csv')  # creating a file in csv extention

with open('petrolprice.csv', 'wb') as createFile:  # This line will create a csv file under name webcrawler
    filewriter = csv.writer(createFile)

url = "https://www.petrolpricemalaysia.my/fuel-price-history-malaysia/"
req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Chrome/35.0.1916.47'})

soup = BeautifulSoup(urllib.request.urlopen(req).read(), "lxml")

# extract data
rows = soup.find('table', {'class': 'genTbl closedTbl historicalTbl'}).findAll('tr')[1:]
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip(' ') for ele in cols]
    data.append([ele for ele in cols if ele])

# extract column names
colnames = soup.find('table', {'class': 'genTbl closedTbl historicalTbl'}).findAll('tr')[:1]
col_names = []
for col in colnames:
    cols = col.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    col_names.append(cols)
col_names = col_names[0]

# Write data to files
df1 = pd.DataFrame(data, columns=col_names)
df1.to_csv('petrolprice.csv', mode='w', index=False)
df1