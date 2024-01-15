import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(os.getenv("MODEL_NAME"))
model.save("model")
