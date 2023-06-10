from sentence_transformers import SentenceTransformer, util
import json
import torch
import numpy
owner = "modelmapper"
repo = "modelmapper"
data = []

with open(f'../assets/data/{owner}_{repo}.json', "r") as f:
    data = json.load(f)['pulls']

# embedder = SentenceTransformer('all-MiniLM-L6-v2')
# embedder = SentenceTransformer('msmarco-MiniLM-L6-cos-v5') # Models tuned with normalized embeddings
# Models tuned for dot-product
embedder = SentenceTransformer('all-mpnet-base-v2')
corpus = []
# Corpus with example sentences
for item in data:
    corpus.append(item['title']+item['body'])
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=False)
print(type(corpus_embeddings))
# numpy.save(f'../assets/data/{owner}_{repo}_corpus_embeddings.npy', corpus_embeddings)
torch.save(corpus_embeddings, f'../assets/data/{owner}_{repo}_corpus_embeddings.pth')
