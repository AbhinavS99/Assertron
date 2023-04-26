import os
import torch
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from unixcoder import UniXcoder
from tqdm import tqdm

def getTopN(n, query_method_embedding, methods, embeddings):
    sim_vals = []
    for embedding in embeddings:
        sim_vals.append(cosine_similarity(embedding, query_method_embedding))

    sorted_embs = sorted(zip(sim_vals, methods, embeddings), reverse=True, key=lambda x: x[0])
    sim_vals, methods, embeddings = map(list, zip(*sorted_embs))
    topNsims, topNmethods, topNembs = sim_vals[:n], methods[:n], embeddings[:n]
    return topNsims, topNmethods, topNembs
    

def build_query(query_method, n=0, type="naive"):
    if type == "naive":
        return f'''
        Add assertion using the assert keyword in the given JAVA method and return the method with the added assertions.
        Method:
            
        {query_method}
        '''
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = UniXcoder("microsoft/unixcoder-base")
    model.to(device)

    tokens_ids = model.tokenize([query_method],max_length=512,mode="<encoder-only>")
    source_ids = torch.tensor(tokens_ids).to(device)
    _, query_method_embedding = model(source_ids)
    query_method_embedding = query_method_embedding.detach().numpy()

    methods, embeddings = joblib.load("/Users/shsabhin/Desktop/assert_ext/backend/dataset/dataset.pkl")
    topNsims, topNmethods, topNembs = getTopN(n, query_method_embedding, methods, embeddings)
    
    return f'''
    The following are the example JAVA methods with assertion.
    
    Example 1:
    {topNmethods[0]}

    Example 2:
    {topNmethods[1]}

    Example 3:
    {topNmethods[2]}

    Now, add assertions in the following JAVA method as in the examples above using the assert keyword. Return the method with the added assertions.
    Method:
    ${query_method}
    '''
    