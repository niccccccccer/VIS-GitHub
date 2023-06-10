from sentence_transformers import SentenceTransformer, util
import json
import numpy as np
import time
import torch
owner = "modelmapper"
repo = "modelmapper"
data = []

with open(f'../assets/data/{owner}_{repo}_pulls.json', "r") as f:
    data = json.load(f)

# embedder = SentenceTransformer('all-MiniLM-L6-v2')
# embedder = SentenceTransformer('msmarco-MiniLM-L6-cos-v5') # Models tuned with normalized embeddings
# Models tuned for dot-product
embedder = SentenceTransformer('msmarco-distilbert-base-tas-b')
corpus = []
# Corpus with example sentences
for item in data:
    corpus.append(item['title']+item['body'])
corpus_embeddings = torch.load(f'../assets/data/{owner}_{repo}_corpus_embeddings.pth')
# corpus_embeddings = np.load(f'../assets/data/{owner}_{repo}_corpus_embeddings.npy')
# corpus_embeddings = np.array(corpus_embeddings)
print(type(corpus_embeddings))

# corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
map = dict((i, item['number']) for i,item in enumerate(data))
# Query sentences:
query = 'go'

# Find the closest 10 sentences of the corpus for each query sentence based on cosine similarity
top_k = min(10, len(corpus))

query_embedding = embedder.encode(query, convert_to_tensor=True)
corpus_embeddings=torch.tensor(corpus_embeddings)
# print("\n\n======================")
# print("Query:", query)
# print("Top 10 most similar sentences in corpus:")

# We use cosine-similarity and torch.topk to find the highest 5 scores
# cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
# top_results = torch.topk(cos_scores, k=top_k)
# for score, idx in zip(top_results[0], top_results[1]):
#     print(idx,corpus[idx], "(Score: {:.4f})".format(score))

# start_time = time.time()
# # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
hits = util.semantic_search(
    query_embedding, corpus_embeddings, top_k=top_k)
hits = hits[0]  # Get the hits for the first query
for hit in hits:
    print(hit['corpus_id'], corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))

# end_time = time.time()
    # print("%d  %sThe number of pr is %d.\nTotal time taken in seconds:%f" %(i,repo,len(data),end_time - start_time))
