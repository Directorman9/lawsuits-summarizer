import requests
from requests.auth import HTTPBasicAuth 

headers = {'user-agent': 'my-app/0.0.1', }
files = {'file': open('report.xls', 'rb')}                                 #if you wish to embed a file
json = {'prompt': ""}                                             #json to be sent with post requests
params = {'name': 'rahma'}                                                 #parameters to be sent with get requ


resp = requests.post(url, json=json, files=files, headers=headers, auth=auth)
resp = requests.get(url, params=params)
