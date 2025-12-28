import logging
from project.components.youtube_extractor import extract_video_id, fetch_transcript, InvalidYouTubeURL, TranscriptNotFound
from project.components.chunker import chunk_text, join_docs, printPrompt
from project.components.embeddings import get_embeddings
from project.components.vectorStore import create_faiss, debug_docs
from project.components.llm import get_llm

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import PromptTemplate
from project.logger import logging

class RAGPipeline:
    def __init__(self):
        self.chain = None

    def _build_prompt(self):
        return PromptTemplate(
            input_variables=["context", "question"],
            template="""
                    You are a helpful assistant answering questions from a YouTube video transcript.

                    Context:
                    {context}

                    Question:
                    {question}

                    Instructions:
                    - Use the context as the primary source.
                    - If the context contains partial information, infer carefully to provide a helpful answer.
                    - If the answer is completely missing from the context, say "I don't know".

                    Answer:

                    """
        )

    def load_video(self, url: str):
        logging.info("---------------Loading video---------------")
        try:
            video_id = extract_video_id(url)
            logging.info(f"Extracted Video ID: {video_id}")
            transcript = fetch_transcript(video_id)
            logging.info("Fetched transcript successfully")
            chunks = chunk_text(transcript)
            logging.info(f"Chunked transcript into {len(chunks)} chunks")
            embeddings = get_embeddings()
            vectorstore = create_faiss(chunks, embeddings)
            logging.info("Created vector store successfully")
            retriever = vectorstore.as_retriever(search_kwargs={"k":12})
            logging.info("Built retriever successfully")   


            prompt = self._build_prompt()
            llm = get_llm()
            parallel = RunnableParallel(
                context=retriever
                        | RunnableLambda(debug_docs)   # 👈 ADD THIS
                        | RunnableLambda(join_docs),
                question=RunnablePassthrough()
            )

            self.chain = parallel| prompt|RunnableLambda(printPrompt)| llm
            logging.info("Video loaded successfully")
        except (InvalidYouTubeURL, TranscriptNotFound) as e:
            logging.error(str(e))
            raise

    def ask(self, question: str) -> str:
        if not self.chain:
            raise Exception("Load a video first")
        logging.info("Processing user question")
        return self.chain.invoke(question)

if __name__ == "__main__":
    
    pipeline = RAGPipeline()
    youtube_url = input("Enter YouTube URL: ")
    logging.info(f"User provided URL: {youtube_url}")   
    try:
        pipeline.load_video(youtube_url)
        logging.info("Entering question-answer loop")
        while True:
            user_question = input("Ask a question (or type 'exit' to quit): ")
            if user_question.lower() == 'exit':
                break
            answer = pipeline.ask(user_question)
            print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error: {e}")