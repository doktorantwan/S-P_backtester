import os
import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=VBL877TP5ZSBSLUH'
r = requests.get(url)
data = r.json()

print(data)