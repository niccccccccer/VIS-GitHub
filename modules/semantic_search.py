from flask_restful import Resource
from sentence_transformers import SentenceTransformer, util
import json
from flask import request
import torch

class SemanticSearch(Resource):
    def post(self):
        # Get the data from the request
        data = request.get_json()
        query = data['query']
        owner = data['owner']
        repo = data['repo']
        # Load data from JSON file
        with open(f'../assets/data/{owner}_{repo}.json', "r") as f:
            data = json.load(f)['pulls']
        corpus=[]
        for item in data:
            corpus.append(item['title'])
        
        map = dict((i, item['number']) for i,item in enumerate(data))

        # Load pre-computed corpus embeddings
        corpus_embeddings=torch.load(f'../assets/data/{owner}_{repo}_corpus_embeddings.pth')
        print("request the semantic search for%s-%s and the query is%s" %(owner, repo, query))
       
        # get the embeddings for the query
        embedder = SentenceTransformer('all-mpnet-base-v2') # Models tuned for dot-product
        # msmarco-distilbert-base-tas-b
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        
        # Find top k similar sentences to query
        top_k = min(10, len(data))
        
        # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
        hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
        hits = hits[0] 

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        # cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        # top_results = torch.topk(cos_scores, k=top_k)
        # for score, idx in zip(top_results[0], top_results[1]):
        #     print(corpus[idx], "(Score: {:.4f})".format(score))

        # Return results as a list of dictionaries
        results = []
        for hit in hits:
            result = {"id":hit['corpus_id'],"number":map[hit['corpus_id']],"title": corpus[hit['corpus_id']], "score": hit['score']}
            results.append(result)
        # print(results)
        return results
