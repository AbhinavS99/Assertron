import os
import glob
import torch
import joblib
from unixcoder import UniXcoder
from tqdm import tqdm

def get_method(method_file):
    f = open(method_file, "r")
    data = f.read()
    data=data.replace("]]],",",,,,")
    data=data.replace("[[[",",,,,")
    data=data.split(',,,,')
    data = list(filter(None, data))
    method=data[0]
    return method

def generateEmbedding(method, model):
    tokens_ids = model.tokenize([method],max_length=512,mode="<encoder-only>")
    source_ids = torch.tensor(tokens_ids).to(device)
    _, max_func_embedding = model(source_ids)
    return max_func_embedding.detach().numpy()

def save_dataset(methods, embeddings):
    store = (methods, embeddings)
    joblib.dump(store, "dataset/dataset.pkl")

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UniXcoder("microsoft/unixcoder-base")
    model.to(device)

    pwd = os.getcwd()
    path = pwd + "/methods/*.txt"
    method_files = sorted(glob.glob(path))
    methods, embeddings = [], []
    for method_file in tqdm(method_files):
        method = get_method(method_file)
        embedding = generateEmbedding(method, model)
        methods.append(method)
        embeddings.append(embedding)

    save_dataset(methods, embeddings)
    print("[+] Complete")
