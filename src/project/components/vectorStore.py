from project.logger import logging  
from langchain_community.vectorstores import FAISS
from project.components.chunker import chunk_text, join_docs
from project.components.embeddings import get_embeddings
from project.components.youtube_extractor import fetch_transcript

def create_faiss(chunks, embeddings):
    return FAISS.from_texts(chunks, embeddings)

def debug_docs(docs):
    logging.info(f"Retrieved {len(docs)} documents")
    for i, d in enumerate(docs):
        logging.info(f"Doc {i} preview: {d.page_content[:300]}")
    return docs


if __name__=="__main__":

            video_id = "0LE5XrxGvbo" 
            print(f"Extracted Video ID: {video_id}")
            transcript = fetch_transcript(video_id)
            print("Fetched transcript successfully")
            chunks = chunk_text(transcript)
            print(f"Chunked transcript into {len(chunks)} chunks")
            embeddings = get_embeddings()
            vectorstore = create_faiss(chunks, embeddings)
            print("Created vector store successfully")
            retriever = vectorstore.as_retriever(search_kwargs={"k":4})
            print("Built retriever successfully")   
            
            query = "What is this video about?"
            docs = retriever.invoke(query)
            print(f"Retrieved {len(docs)} documents")
            print(join_docs(docs))