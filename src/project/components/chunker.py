from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def join_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
