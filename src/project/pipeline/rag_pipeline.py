import logging
from ..components.youtube_extractor import extract_video_id, fetch_transcript, InvalidYouTubeURL, TranscriptNotFound
from ..components.chunker import chunk_text, join_docs
from ..components.embeddings import get_embeddings
from ..components.vectorstore import create_faiss
from ..components.llm import get_llm

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.chain = None

    def _build_prompt(self):
        return PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful assistant.
                        Answer ONLY using the context below.
                        If the answer is not present, say "I don't know".

                        Context:
                        {context}

                        Question:
                        {question}

                        Answer:
                        """
        )

    def load_video(self, url: str):
        logger.info("Loading video...")
        try:
            video_id = extract_video_id(url)
            transcript = fetch_transcript(video_id)
            chunks = chunk_text(transcript)
            embeddings = get_embeddings()
            vectorstore = create_faiss(chunks, embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k":4})
            prompt = self._build_prompt()
            llm = get_llm()
            parallel = RunnableParallel(
                context=retriever | RunnableLambda(join_docs),
                question=RunnablePassthrough()
            )
            self.chain = parallel | prompt | llm
            logger.info("Video loaded successfully")
        except (InvalidYouTubeURL, TranscriptNotFound) as e:
            logger.error(str(e))
            raise

    def ask(self, question: str) -> str:
        if not self.chain:
            raise Exception("Load a video first")
        logger.info("Processing user question")
        return self.chain.invoke(question)
