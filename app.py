import streamlit as st
from src.project.pipeline.rag_pipeline import RAGPipeline

st.set_page_config(page_title="YouTube RAG Chatbot", layout="wide")
st.title("YouTube RAG Chatbot (Streamlit)")

pipeline = RAGPipeline()

# Step 1: Load Video
video_url = st.text_input("Enter YouTube URL to load transcript")

if st.button("Load Video"):
    if not video_url:
        st.warning("Please enter a YouTube URL")
    else:
        try:
            with st.spinner("Loading video..."):
                pipeline.load_video(video_url)
            st.success("Video loaded successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Step 2: Ask questions
if pipeline.chain:
    question = st.text_input("Ask a question about the video")
    if st.button("Ask"):
        if not question:
            st.warning("Please enter a question")
        else:
            try:
                with st.spinner("Generating answer..."):
                    answer = pipeline.ask(question)
                st.write("**Answer:**", answer)
            except Exception as e:
                st.error(f"Error: {str(e)}")
