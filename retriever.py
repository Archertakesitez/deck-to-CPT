from transformers import AutoTokenizer, AutoModel
import torch
import pickle
import faiss

with open("sentence_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

# Retrieve sentences and embeddings
sentences = data["sentences"]
sentence_embeddings = data["embeddings"]

dimension = sentence_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
index.add(sentence_embeddings)


def retrieve_similar_sentences(query, top_k=5):
    # Encode the query
    query_embedding = encode_sentences([query])
    
    # Search for top_k most similar sentences
    distances, indices = index.search(query_embedding, top_k)
    
    # Fetch and return the most similar sentences
    results = []
    for idx in indices[0]:
        results.append(sentences[idx])
    return results

query = "Enter your query here"
similar_sentences = retrieve_similar_sentences(query, top_k=5)
print("Top similar sentences:")
for sentence in similar_sentences:
    print(sentence)