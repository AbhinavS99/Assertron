import pickle
import joblib
import json
import requests
import base64

update_url = 'https://api.github.com/repos/AbhinavS99/AssertGen/contents/store.pkl?ref=eval'
headers = {'Authorization': 'token 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', 'Content-Type': 'application/json'}

data = joblib.load("store.pkl")
updated_content = pickle.dumps(data)
encoded_content = base64.b64encode(updated_content).decode('utf-8')
response = requests.get(update_url, headers=headers)
sha = json.loads(response.content)['sha']
data = {
        "message": "Update file",
        "content": encoded_content,
        "sha": sha,
        "branch": "eval"
    }
update_response = requests.put(update_url, headers=headers, data=json.dumps(data))
print(update_response)
if response.status_code == 200:
    print('File updated successfully.')
else:
    print('Failed to update the file.')