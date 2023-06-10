import json
from flask_restful import Resource
from sentence_transformers import SentenceTransformer, util
from flask import request
import torch

owner = 'modelmapper'
repo = 'modelmapper'
data=[]
method='TSNE'

with open(f'../assets/data/{owner}_{repo}_pulls.json', "r") as f:
    data = json.load(f)
map = dict((i, item['number']) for i,item in enumerate(data))
# query="null pointer exception"
query="fixconfiguration"
model = SentenceTransformer('msmarco-distilbert-base-tas-b')
embedding = model.encode(query, convert_to_tensor=True)

embeddings=torch.load(f'../assets/data/{owner}_{repo}_corpus_embeddings.pth')
embeddings=torch.tensor(embeddings)
print(embeddings.shape)
print(embedding.shape)
embeddings = torch.cat((embeddings, embedding.unsqueeze(0)), dim=0)
print(embeddings.shape)
print("request the dimensionality ruduction for%s-%s and the query is%s" %(owner, repo, query))

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
#---------------TSNE-------------------
def prepocessing_tsne(data, n):
    dataset = TSNE(n_components=n, random_state=33).fit_transform(data)
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_tsne = scaler.fit_transform(dataset)
    return X_tsne
#---------------PCA-------------------
def prepocessing_pca(data, n):
    dataset = PCA(n_components=n).fit_transform(data)
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_pca = scaler.fit_transform(dataset) 
    return X_pca
digits_tsne = []
digits_pca = []

if method == 'TSNE':
    digits_tsne = prepocessing_tsne(embeddings, 2)
    print(type(digits_tsne))
    print(digits_tsne.shape)
    print( digits_tsne[0])
else:
    digits_pca = prepocessing_pca(embeddings, 2)
    print(type(digits_pca))
    print(digits_pca.shape)
    print(digits_pca)
  
        
