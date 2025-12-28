import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
  return text_splitter.split_text(text)

def join_docs(docs):
    # Just join text without the [Chunk x] labels
    return "\n".join(doc.page_content for doc in docs)

def printPrompt(message):
    # print(message)
    return message

if __name__ == "__main__":
   chunks = chunk_text("hello world " * 100)
   print(chunks)
   print(f"Number of chunks: {len(chunks)}")
