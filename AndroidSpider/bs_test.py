
import requests

params = {'id': 'ctl00', }
r = requests.post("https://etherscan.io/txsInternal?a=0x7751278c8b6b224946d065776fc67c81a5202958&&valid=true&p=1", data=params)
print(r.text('a'))