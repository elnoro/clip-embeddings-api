from sentence_transformers import SentenceTransformer

model = SentenceTransformer('clip-ViT-B-32')
model.save("model")