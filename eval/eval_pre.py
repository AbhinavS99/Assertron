import sys
sys.path.append('../')

import re
import os
import glob
import torch
import joblib
from unixcoder import UniXcoder
from tqdm import tqdm

def removeAsserts(method):
    matches = re.findall(r'assert.*;', method)
    for matchi in matches:
        method=method.replace(matchi, " ")
        method = os.linesep.join([s for s in method.splitlines() if s.strip()])
    return method

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

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UniXcoder("microsoft/unixcoder-base")
    model.to(device)

    path = "../test_methods/*.txt"
    method_files = sorted(glob.glob(path))
    orig_methods, methods, embeddings = [], [], []
    count = 0
    for method_file in tqdm(method_files):
        orig_method = get_method(method_file)
        method = removeAsserts(orig_method)
        embedding = generateEmbedding(method, model)
        orig_methods.append(orig_method)
        methods.append(method)
        embeddings.append(embedding)
        count += 1
        if count == 3:
            break

    store = []
    for i in tqdm(range(0, len(methods))):
        val = {}
        val["index"] = i
        val["author"] = ""
        val["method"] = methods[i]
        val["ground_truth"] = orig_methods[i]
        val["embedding"] = embeddings[i]
        val["naive_op"] = ""
        val["few_shot_op"] = ""

        val["fs_wrong_variable"] = ""
        val["fs_wrong_variable_comment"] = ""
        val["fs_wrong_method_called"] = ""
        val["fs_wrong_method_called_comment"] = ""
        val["fs_wrong_syntax"] = ""
        val["fs_wrong_syntax_comment"] = ""
        val["fs_any_other_syntax_comment"] = ""
        val["fs_weak_assert"] = ""
        val["fs_weak_assert_comment"] = ""
        val["fs_new_info"] = ""
        val["fs_new_info_comment"] = ""
        val["fs_wrong_location"] = ""
        val["fs_wrong_location_comment"] = ""
        val["fs_wrong_assumption"] = ""
        val["fs_wrong_assumption_comment"] = ""
        val["fs_all_covered"] = ""
        val["fs_partial_covered"] = ""
        val["fs_none_covered"] = ""
       
        val["nv_wrong_variable"] = ""
        val["nv_wrong_variable_comment"] = ""
        val["nv_wrong_method_called"] = ""
        val["nv_wrong_method_called_comment"] = ""
        val["nv_wrong_syntax"] = ""
        val["nv_wrong_syntax_comment"] = ""
        val["nv_any_other_syntax_comment"] = ""
        val["nv_weak_assert"] = ""
        val["nv_weak_assert_comment"] = ""
        val["nv_new_info"] = ""
        val["nv_new_info_comment"] = ""
        val["nv_wrong_location"] = ""
        val["nv_wrong_location_comment"] = ""
        val["nv_wrong_assumption"] = ""
        val["nv_wrong_assumption_comment"] = ""
        val["nv_all_covered"] = ""
        val["nv_partial_covered"] = ""
        val["nv_none_covered"] = ""
        
        store.append(val)

joblib.dump(store, "store.pkl")
print("Init Store Created")