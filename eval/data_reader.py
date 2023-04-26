import pickle
import joblib
import requests
import json

url = 'https://raw.githubusercontent.com/AbhinavS99/AssertGen/eval/store.pkl'
headers = {'Authorization': 'token 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', 'Content-Type': 'application/json'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    file_content = response.content
    data = pickle.loads(file_content)
    print('Data Items:', len(data))
    joblib.dump(data, "store.pkl")