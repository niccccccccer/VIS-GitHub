import json
from flask_restful import Resource
from sentence_transformers import SentenceTransformer, util
from flask import request
import torch

class DimensionalityReduction(Resource):
    def post(self):
        data = request.get_json()
        query = data['query']
        owner = data['owner']
        repo = data['repo']
        pulls=[]
        method='TSNE'

        with open(f'../assets/data/{owner}_{repo}.json', "r") as f:
            pulls = json.load(f)['pulls']
        map = dict((i, item['number']) for i,item in enumerate(pulls))

        model = SentenceTransformer('all-mpnet-base-v2')
        embedding = model.encode(query, convert_to_tensor=True)

        embeddings=torch.load(f'../assets/data/{owner}_{repo}_corpus_embeddings.pth')
        embeddings=torch.tensor(embeddings)
        embeddings = torch.cat((embeddings, embedding.unsqueeze(0)), dim=0)
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
        def getJson(data):
            data=data.tolist()
            result=[]
            index=0
            print(data[0])
            for item in data:
                if(index==0):
                    result.append({'x':item[0],'y':item[1],'index':index-1,'title':"query"+query,'number':"None"})
                else:
                    result.append({'x':item[0],'y':item[1],'index':index-1,'title':pulls[index-1]['title'],'number':pulls[index-1]['number']})
                index=index+1
            result= json.dumps(result)
            return result

        if method == 'TSNE':
            digits_tsne = prepocessing_tsne(embeddings, 2)
            print(type(digits_tsne))
            print(digits_tsne.shape)
            result= getJson(digits_tsne)
            return result
        else:
            digits_pca = prepocessing_pca(embeddings, 2)
            print(type(digits_pca))
            print(digits_pca.shape)
            result= getJson(digits_pca)
            return result
  
        
