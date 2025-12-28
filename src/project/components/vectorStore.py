from langchain_community.vectorstores import FAISS

def create_faiss(chunks, embeddings):
    return FAISS.from_texts(chunks, embeddings)
