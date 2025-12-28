from langchain_community.llms import Ollama

def get_llm():
    return Ollama(model="phi4-mini", temperature=0.2)

if __name__ == "__main__":
    llm=get_llm()
    print(llm.invoke("who is Virat Kohli"))