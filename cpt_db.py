from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import faiss
import pickle

# Load CSV
def load_data(csv:str):
    df = pd.read_csv(csv)  # replace with your actual file
    sentences = df['sentence'].tolist()
    return sentences

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-base-en-v1.5")
model = AutoModel.from_pretrained("BAAI/bge-base-en-v1.5")

# Define an encoding function
def encode_sentences(sentences):
    inputs = tokenizer(sentences, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use CLS token representation for sentence embedding
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings

# Encode all sentences
sentences = load_data('place_hoder.csv')
sentence_embeddings = encode_sentences(sentences)

# Store sentences and embeddings in a dictionary
data = {
    "sentences": sentences,
    "embeddings": sentence_embeddings
}

# Save to a pickle file
with open("sentence_embeddings.pkl", "wb") as f:
    pickle.dump(data, f)