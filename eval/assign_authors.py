import sys
sys.path.append('../')

import joblib
from tqdm import tqdm

store = joblib.load("store.pkl")
aditi = [0, 20]
reshmi = [21, 40]
abhinav = [41, 60]
for item in tqdm(store):
    if aditi[0] <= item["index"] <= aditi[1]:
        item["author"] = "aditi"

    if reshmi[0] <= item["index"] <= reshmi[1]:
        item["author"] = "reshmi"

    if abhinav[0] <= item["index"] <= abhinav[1]:
        item["author"] = "abhinav"

joblib.dump(store, "store.pkl")