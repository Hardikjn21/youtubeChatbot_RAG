from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
  return text_splitter.split_text(text)

def join_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
   chunks = chunk_text("hello world " * 100)
   print(chunks)
   print(f"Number of chunks: {len(chunks)}")
