import streamlit as st
from src.project.pipeline.rag_pipeline import RAGPipeline

st.set_page_config(page_title="YouTube RAG Chatbot", layout="wide")
st.title("YouTube RAG Chatbot (Streamlit)")

# Initialize pipeline in session_state
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

# Step 1: Load Video
video_url = st.text_input("Enter YouTube URL to load transcript")

if st.button("Load Video"):
    if not video_url:
        st.warning("Please enter a YouTube URL")
    else:
        try:
            with st.spinner("Loading video..."):
                st.session_state.pipeline.load_video(video_url)
            st.session_state.video_loaded = True
            st.success("Video loaded successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Step 2: Ask questions (only if video is loaded)
if st.session_state.video_loaded:
    question = st.text_input("Ask a question about the video", key="question_input")
    if st.button("Ask"):
        if not question:
            st.warning("Please enter a question")
        else:
            try:
                with st.spinner("Generating answer..."):
                    answer = st.session_state.pipeline.ask(question)
                st.markdown(f"**Answer:** {answer}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
