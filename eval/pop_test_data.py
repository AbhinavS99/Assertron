import sys
sys.path.append('../')

import joblib
import openai
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

from tqdm import tqdm
from query_builder import build_query
store = joblib.load("store.pkl")

for item in tqdm(store):
    few_shot_query = build_query(item["method"], 3, "fewShot")
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": ""},
                          {"role": "user", "content": few_shot_query}],
                temperature=0,
                max_tokens=1023,
                presence_penalty=-0.5,
                n=1)
    op = response.choices[0].message.content
    item["few_shot_op"] = op

    naive_query = build_query(item["method"])
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": ""},
                          {"role": "user", "content": naive_query}],
                temperature=0,
                max_tokens=1023,
                presence_penalty=-0.5,
                n=1)
    op = response.choices[0].message.content
    item["naive_op"] = op

joblib.dump(store, "store.pkl")