"""
Study Mate Bot - Streamlit Frontend
Interactive UI for document upload, Q&A, and quiz generation
"""

import streamlit as st
import requests
import json
import time
from typing import List, Dict, Any
import os

# Configure page
st.set_page_config(
    page_title="Study Mate Bot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

class StudyMateBot:
    """Main application class"""
    
    def __init__(self):
        self.api_url = API_BASE_URL
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        if "quiz_questions" not in st.session_state:
            st.session_state.quiz_questions = []
        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}
        if "current_mode" not in st.session_state:
            st.session_state.current_mode = "chat"
    
    def check_api_health(self) -> bool:
        """Check if API is running"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def upload_document(self, file) -> Dict[str, Any]:
        """Upload document to API"""
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(f"{self.api_url}/upload", files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Upload failed: {response.text}"}
        except Exception as e:
            return {"error": f"Upload error: {str(e)}"}
    
    def ask_question(self, question: str, num_sources: int = 4) -> Dict[str, Any]:
        """Ask question to API"""
        try:
            payload = {
                "question": question,
                "num_sources": num_sources
            }
            response = requests.post(f"{self.api_url}/ask", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Question failed: {response.text}"}
        except Exception as e:
            return {"error": f"Question error: {str(e)}"}
    
    def generate_summary(self, summary_type: str = "full") -> Dict[str, Any]:
        """Generate summary from API"""
        try:
            payload = {"summary_type": summary_type}
            response = requests.post(f"{self.api_url}/summarize", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Summary failed: {response.text}"}
        except Exception as e:
            return {"error": f"Summary error: {str(e)}"}
    
    def generate_quiz(self, num_questions: int = 5, quiz_type: str = "mixed") -> Dict[str, Any]:
        """Generate quiz from API"""
        try:
            payload = {
                "num_questions": num_questions,
                "quiz_type": quiz_type
            }
            response = requests.post(f"{self.api_url}/quiz", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Quiz generation failed: {response.text}"}
        except Exception as e:
            return {"error": f"Quiz error: {str(e)}"}
    
    def clear_memory(self) -> bool:
        """Clear conversation memory"""
        try:
            response = requests.delete(f"{self.api_url}/clear-memory")
            return response.status_code == 200
        except:
            return False

def main():
    """Main application"""
    bot = StudyMateBot()
    
    # Header
    st.title("Study Mate Bot")
    st.markdown("**Your AI-powered study assistant with RAG capabilities**")
    
    # Check API health
    if not bot.check_api_health():
        st.error("API server is not running! Please start the backend server first.")
        st.code("cd backend && python main.py")
        return
    
    st.success("Connected to API server")
    
    # Sidebar
    with st.sidebar:
        st.header("Controls")
        
        # Mode selection
        mode = st.radio(
            "Select Mode:",
            ["chat", "quiz", "summary"],
            index=["chat", "quiz", "summary"].index(st.session_state.current_mode)
        )
        st.session_state.current_mode = mode
        
        st.divider()
        
        # Document upload
        st.subheader("📄 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Upload PDF, TXT, or DOCX files for study"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                if file.name not in [f["filename"] for f in st.session_state.uploaded_files]:
                    with st.spinner(f"Uploading {file.name}..."):
                        result = bot.upload_document(file)
                        if "error" not in result:
                            st.session_state.uploaded_files.append({
                                "filename": file.name,
                                "chunks": result["chunks"],
                                "total_docs": result["chunks"]
                            })
                            st.success(f"{file.name} uploaded!")
                        else:
                            st.error(f"{result['error']}")
        
        # Display uploaded files
        if st.session_state.uploaded_files:
            st.subheader("📋 Uploaded Files")
            for file_info in st.session_state.uploaded_files:
                st.write(f"📄 {file_info['filename']}")
                st.caption(f"Chunks: {file_info['chunks']}")
        
        st.divider()
        
        # Memory controls
        st.subheader("🧠 Memory")
        if st.button("Clear Conversation Memory"):
            if bot.clear_memory():
                st.session_state.messages = []
                st.success("Memory cleared!")
            else:
                st.error("Failed to clear memory")
    
    # Main content area
    if mode == "chat":
        chat_interface(bot)
    elif mode == "quiz":
        quiz_interface(bot)
    elif mode == "summary":
        summary_interface(bot)

def chat_interface(bot: StudyMateBot):
    """Chat interface for Q&A"""
    st.header("Chat with Your Study Materials")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if "sources" in message and message["sources"]:
                with st.expander("Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.write(f"**Source {i+1}:** {source['metadata'].get('source', 'Document')}")
                        st.write(source["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your study materials..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = bot.ask_question(prompt)
                
                if "error" not in response:
                    st.markdown(response["answer"])
                    
                    # Show sources
                    if response["sources"]:
                        with st.expander("Sources"):
                            for i, source in enumerate(response["sources"]):
                                st.write(f"**Source {i+1}:** {source['metadata'].get('source', 'Document')}")
                                st.write(source["content"])
                    
                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"]
                    })
                else:
                    st.error(f"Error: {response['error']}")

def quiz_interface(bot: StudyMateBot):
    """Quiz interface"""
    st.header("🧠 Quiz Mode")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generate Quiz")
        
        num_questions = st.slider("Number of questions", 1, 10, 5)
        quiz_type = st.selectbox(
            "Quiz type",
            ["mixed", "multiple_choice", "true_false", "short_answer"]
        )
        
        if st.button("Generate Quiz", type="primary"):
            with st.spinner("Generating quiz questions..."):
                response = bot.generate_quiz(num_questions, quiz_type)
                
                if "error" not in response:
                    st.session_state.quiz_questions = response["questions"]
                    st.success(f"Generated {len(response['questions'])} questions!")
                else:
                    st.error(f"Error: {response['error']}")
    
    with col2:
        st.subheader("Quiz Settings")
        if st.button("🔄 Reset Quiz"):
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.rerun()
    
    # Display quiz questions
    if st.session_state.quiz_questions:
        st.subheader("Quiz Questions")
        
        for i, question in enumerate(st.session_state.quiz_questions):
            with st.container():
                st.write(f"**Question {i+1}:** {question['question']}")
                
                if question["type"] == "multiple_choice":
                    answer = st.radio(
                        f"Options for Q{i+1}:",
                        question["options"],
                        key=f"q{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[f"q{i}"] = answer
                
                elif question["type"] == "true_false":
                    answer = st.radio(
                        f"True/False for Q{i+1}:",
                        ["True", "False"],
                        key=f"q{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[f"q{i}"] = answer
                
                elif question["type"] == "short_answer":
                    answer = st.text_input(
                        f"Your answer for Q{i+1}:",
                        key=f"q{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[f"q{i}"] = answer
                
                # Show correct answer and explanation
                if st.button(f"Show Answer {i+1}", key=f"show{i}"):
                    st.info(f"**Correct Answer:** {question['correct_answer']}")
                    st.write(f"**Explanation:** {question['explanation']}")
                
                st.divider()

def summary_interface(bot: StudyMateBot):
    """Summary interface"""
    st.header("📋 Document Summary")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        summary_type = st.selectbox(
            "Summary type",
            ["full", "section"],
            help="Full: Complete summary, Section: Summary by sections"
        )
    
    with col2:
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Generating summary..."):
                response = bot.generate_summary(summary_type)
                
                if "error" not in response:
                    st.subheader("📄 Summary")
                    st.markdown(response["summary"])
                else:
                    st.error(f"Error: {response['error']}")

if __name__ == "__main__":
    main()
