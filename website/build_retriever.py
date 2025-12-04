from pathlib import Path
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load chunk files
chunk_dir = Path("chunks")
chunk_files = sorted(chunk_dir.glob("chunk_*.txt"))

documents = [f.read_text(encoding="utf-8") for f in chunk_files]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=40000
)

X = vectorizer.fit_transform(documents)

# Save everything to a single file
with open("retriever.pkl", "wb") as f:
    pickle.dump({
        "vectorizer": vectorizer,
        "X": X,
        "documents": documents,
        "files": [str(f) for f in chunk_files]
    }, f)

print("Retriever created → retriever.pkl saved!")
