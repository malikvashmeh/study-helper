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
        if "show_doc_manager" not in st.session_state:
            st.session_state.show_doc_manager = False
        if "selected_documents" not in st.session_state:
            st.session_state.selected_documents = set()
    
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
            data = {"mode": "add"}
            response = requests.post(f"{self.api_url}/upload", files=files, data=data)
            
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
        """Clear conversation memory only"""
        try:
            response = requests.delete(f"{self.api_url}/clear-memory")
            return response.status_code == 200
        except:
            return False
    
    def clear_all_documents(self) -> Dict[str, Any]:
        """Clear all documents and reset RAG memory completely"""
        try:
            response = requests.delete(f"{self.api_url}/clear-documents")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Clear failed: {response.text}"}
        except Exception as e:
            return {"error": f"Clear error: {str(e)}"}
    
    def replace_all_documents(self) -> Dict[str, Any]:
        """Replace all documents with new ones from data folder"""
        try:
            payload = {"force_reprocess": True}
            response = requests.post(f"{self.api_url}/replace-documents", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Replace failed: {response.text}"}
        except Exception as e:
            return {"error": f"Replace error: {str(e)}"}
    
    def get_store_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            response = requests.get(f"{self.api_url}/store-stats")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Stats failed: {response.text}"}
        except Exception as e:
            return {"error": f"Stats error: {str(e)}"}
    
    def list_documents(self) -> Dict[str, Any]:
        """List all documents in memory"""
        try:
            response = requests.get(f"{self.api_url}/list-documents")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"List failed: {response.text}"}
        except Exception as e:
            return {"error": f"List error: {str(e)}"}
    
    def test_memory_reset(self, test_queries: List[str] = None) -> Dict[str, Any]:
        """Test that memory has been properly reset"""
        if test_queries is None:
            test_queries = ["pythagorean theorem", "unit 42", "a² + b² = c²"]
        
        results = {"queries_tested": [], "memory_clean": True}
        
        for query in test_queries:
            try:
                response = self.ask_question(query)
                if "error" not in response:
                    answer = response.get("answer", "").lower()
                    sources = response.get("sources", [])
                    
                    # Check if it correctly shows no information
                    has_no_info = ("no information" in answer or 
                                 "cannot answer" in answer or 
                                 "no relevant documents" in answer)
                    
                    has_no_sources = not sources or all(not src.get("content", "").strip() for src in sources)
                    
                    results["queries_tested"].append({
                        "query": query,
                        "clean_answer": has_no_info,
                        "clean_sources": has_no_sources,
                        "is_clean": has_no_info and has_no_sources
                    })
                    
                    if not (has_no_info and has_no_sources):
                        results["memory_clean"] = False
                        
            except Exception as e:
                results["queries_tested"].append({
                    "query": query,
                    "error": str(e),
                    "is_clean": False
                })
                results["memory_clean"] = False
        
        return results

    def remove_specific_documents(self, document_ids: List[str]) -> Dict[str, Any]:
        """Remove specific documents by their IDs"""
        try:
            # For now, we'll implement this as a clear + reload without the specified docs
            # In a full implementation, you'd have a specific endpoint for this
            payload = {"document_ids": document_ids}
            response = requests.post(f"{self.api_url}/remove-documents", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Remove failed: {response.text}"}
        except Exception as e:
            # Fallback: just return error for now since endpoint doesn't exist yet
            return {"error": f"Document removal not implemented yet: {str(e)}"}
    
    def upload_and_add_document(self, file) -> Dict[str, Any]:
        """Upload document and add to existing collection without clearing"""
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            data = {"mode": "add"}
            response = requests.post(f"{self.api_url}/upload", files=files, data=data)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Upload failed: {response.text}"}
        except Exception as e:
            return {"error": f"Upload error: {str(e)}"}

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
            ["chat", "quiz", "summary", "documents"],
            index=["chat", "quiz", "summary", "documents"].index(st.session_state.current_mode),
            help="Choose your interaction mode"
        )
        st.session_state.current_mode = mode
        
        st.divider()
        
        # Quick Document Upload (always visible)
        st.subheader("📄 Quick Upload")
        uploaded_file = st.file_uploader(
            "Add Document",
            type=['pdf', 'txt', 'docx'],
            help="Upload a single document to add to your knowledge base",
            key="quick_upload"
        )
        
        if uploaded_file:
            if st.button("➕ Add Document", key="add_single_doc"):
                with st.spinner(f"Adding {uploaded_file.name}..."):
                    result = bot.upload_and_add_document(uploaded_file)
                    if "error" not in result:
                        st.success(f"✅ Added {uploaded_file.name}!")
                        st.session_state.uploaded_files.append({
                            "filename": uploaded_file.name,
                            "chunks": result["chunks"],
                            "status": "active"
                        })
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
        
        st.divider()
        
        # Document Manager Toggle
        if st.button("📁 Document Manager", use_container_width=True):
            st.session_state.show_doc_manager = not st.session_state.show_doc_manager
            st.rerun()
        
        # Document Manager Panel
        if st.session_state.show_doc_manager:
            st.subheader("📋 Document Manager")
            
            # Get current documents
            with st.spinner("Loading documents..."):
                docs_response = bot.list_documents()
                
            if "error" not in docs_response:
                current_docs = docs_response.get("documents", [])
                
                if current_docs:
                    st.write(f"**📊 {len(current_docs)} documents in memory**")
                    
                    # Bulk actions
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✅ Select All", key="select_all_docs"):
                            st.session_state.selected_documents = {doc["document_id"] for doc in current_docs}
                            st.rerun()
                    
                    with col2:
                        if st.button("❌ Clear Selection", key="clear_selection"):
                            st.session_state.selected_documents.clear()
                            st.rerun()
                    
                    # Document List with checkboxes
                    for doc in current_docs:
                        doc_id = doc["document_id"]
                        filename = doc["filename"]
                        file_type = doc["file_type"]
                        chunks = doc["chunks_found"]
                        
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            # Checkbox for selection
                            is_selected = st.checkbox(
                                f"📄 **{filename}**",
                                value=doc_id in st.session_state.selected_documents,
                                key=f"select_{doc_id}",
                                help=f"Type: {file_type} | Chunks: {chunks}"
                            )
                            
                            if is_selected:
                                st.session_state.selected_documents.add(doc_id)
                            else:
                                st.session_state.selected_documents.discard(doc_id)
                        
                        with col2:
                            st.caption(f"{file_type}")
                        
                        with col3:
                            st.caption(f"{chunks} chunks")
                    
                    # Bulk Actions
                    if st.session_state.selected_documents:
                        st.write(f"**Selected: {len(st.session_state.selected_documents)} documents**")
                        
                        if st.button("🗑️ Remove Selected", type="secondary", key="remove_selected"):
                            selected_list = list(st.session_state.selected_documents)
                            with st.spinner("Removing selected documents..."):
                                result = bot.remove_specific_documents(selected_list)
                                if "error" not in result:
                                    st.success(f"✅ Removed {len(selected_list)} documents!")
                                    st.session_state.selected_documents.clear()
                                    st.rerun()
                                else:
                                    st.error(f"❌ Removal failed: {result['error']}")
                                    st.info("💡 Try using 'Reset All Memory' for complete cleanup")
                else:
                    st.info("📭 No documents in memory")
                    st.caption("Upload documents above or use the bulk upload below")
            else:
                st.error("Failed to load document list")
        
        st.divider()
        
        # Bulk Document Upload (Enhanced)
        st.subheader("📂 Bulk Upload")
        
        # Upload mode selection
        upload_mode = st.radio(
            "Upload Mode:",
            ["add_to_existing", "replace_all"],
            format_func=lambda x: "➕ Add to Current" if x == "add_to_existing" else "🔄 Replace All",
            help="Choose whether to add documents to current collection or replace everything",
            horizontal=True
        )
        
        uploaded_files = st.file_uploader(
            "Choose multiple files",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Upload multiple documents at once"
        )
        
        if uploaded_files:
            st.write(f"**Ready to upload {len(uploaded_files)} files:**")
            for file in uploaded_files:
                st.caption(f"• {file.name} ({file.size} bytes)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Start Upload", type="primary", use_container_width=True):
                    if upload_mode == "replace_all":
                        # Clear first, then upload
                        with st.spinner("Clearing old documents..."):
                            clear_result = bot.clear_all_documents()
                            if "error" in clear_result:
                                st.error(f"❌ Clear failed: {clear_result['error']}")
                                st.stop()
                            
                        st.success("✅ Old documents cleared!")
                    
                    # Upload new documents
                    success_count = 0
                    error_count = 0
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, file in enumerate(uploaded_files):
                        status_text.text(f"Uploading {file.name}...")
                        result = bot.upload_and_add_document(file)
                        
                        if "error" not in result:
                            success_count += 1
                            st.session_state.uploaded_files.append({
                                "filename": file.name,
                                "chunks": result["chunks"],
                                "status": "active"
                            })
                        else:
                            error_count += 1
                            st.error(f"❌ Failed to upload {file.name}: {result['error']}")
                        
                        progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    status_text.text("Upload complete!")
                    
                    if success_count > 0:
                        st.success(f"✅ Successfully uploaded {success_count} documents!")
                    if error_count > 0:
                        st.warning(f"⚠️ {error_count} documents failed to upload")
                    
                    if success_count > 0:
                        st.rerun()
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.rerun()
        
        st.divider()
        
        # Enhanced Memory controls
        st.subheader("🧠 Memory Management")
        
        # Show current memory status
        if st.button("📊 Show Memory Status", help="View current documents and memory statistics"):
            with st.spinner("Loading memory status..."):
                stats = bot.get_store_stats()
                docs_list = bot.list_documents()
                
                if "error" not in stats and "error" not in docs_list:
                    st.write("**Current Memory Status:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Documents", stats.get('total_documents', 0))
                        st.metric("Unique Files", stats.get('unique_files', 0))
                    
                    with col2:
                        st.metric("Vector DB", stats.get('vector_db_type', 'Unknown'))
                        st.metric("Tracked Docs", stats.get('metadata_tracked_docs', 0))
                    
                    # Show document details
                    if docs_list.get('documents'):
                        with st.expander("📁 Current Documents"):
                            for doc in docs_list['documents'][:5]:  # Show first 5
                                st.write(f"📄 **{doc.get('filename', 'Unknown')}**")
                                st.caption(f"Type: {doc.get('file_type', 'N/A')} | Chunks: {doc.get('chunks_found', 0)}")
                            
                            if len(docs_list['documents']) > 5:
                                st.caption(f"... and {len(docs_list['documents']) - 5} more documents")
                    else:
                        st.info("🔄 Memory is empty - ready for new documents")
                else:
                    st.error("Failed to load memory status")
        
        # Memory action buttons
        st.write("**Memory Actions:**")
        
        # Clear conversation only
        if st.button("💭 Clear Chat Only", help="Clear conversation history but keep documents", use_container_width=True):
            if bot.clear_memory():
                st.session_state.messages = []
                st.success("✅ Chat history cleared!")
            else:
                st.error("❌ Failed to clear chat history")
        
        # Complete memory reset
        if st.button("🧹 RESET ALL MEMORY", help="⚠️ COMPLETE RESET: Clear all documents and chat history", type="primary", use_container_width=True):
            # Confirmation dialog
            if st.session_state.get('confirm_reset', False):
                with st.spinner("🧹 Performing complete memory reset..."):
                    # Clear documents
                    doc_result = bot.clear_all_documents()
                    
                    if "error" not in doc_result:
                        # Clear chat
                        bot.clear_memory()
                        st.session_state.messages = []
                        st.session_state.uploaded_files = []
                        
                        # Test that reset worked
                        test_result = bot.test_memory_reset()
                        
                        if test_result.get("memory_clean", False):
                            st.success("✅ COMPLETE MEMORY RESET SUCCESSFUL!")
                            st.success(f"🔄 Backup created: {doc_result.get('backup_created', 'N/A')}")
                            st.info("💡 Memory is now completely empty and ready for new documents")
                        else:
                            st.warning("⚠️ Reset completed but some old content may persist")
                            
                            # Show test results
                            with st.expander("🧪 Reset Test Results"):
                                for test in test_result.get("queries_tested", []):
                                    status = "✅" if test.get("is_clean", False) else "⚠️"
                                    st.write(f"{status} '{test['query']}': {'Clean' if test.get('is_clean', False) else 'Has residual content'}")
                    else:
                        st.error(f"❌ Reset failed: {doc_result['error']}")
                
                # Reset confirmation flag
                st.session_state.confirm_reset = False
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ Click again to confirm COMPLETE MEMORY RESET")
                st.caption("This will clear ALL documents and chat history (backup will be created)")
                st.rerun()
        
        # Smart document refresh (your main use case)
        if st.button("🔄 Refresh Documents", help="Clear old documents and load new ones from data folder", use_container_width=True):
            with st.spinner("🔄 Refreshing documents with new content..."):
                # Use the replace method for complete refresh
                result = bot.replace_all_documents()
                
                if "error" not in result:
                    # Clear uploaded files list and chat
                    st.session_state.uploaded_files = []
                    st.session_state.messages = []
                    
                    st.success("✅ Documents refreshed successfully!")
                    st.success(f"📄 New documents: {result.get('unique_documents', 0)}")
                    st.success(f"🔢 Total chunks: {result.get('new_document_chunks', 0)}")
                    
                    if result.get('backup_created'):
                        st.info(f"📦 Old documents backed up: {result['backup_created']}")
                    
                    if result.get('errors'):
                        st.warning("⚠️ Some files had errors:")
                        for error in result['errors'][:3]:  # Show first 3 errors
                            st.caption(f"• {error}")
                    
                    # Test the refresh worked
                    with st.spinner("🧪 Verifying document refresh..."):
                        test_result = bot.test_memory_reset()
                        if test_result.get("memory_clean", True):  # True if no old content
                            st.success("✅ Old content successfully removed!")
                        else:
                            st.warning("⚠️ Some old content may still be present")
                else:
                    st.error(f"❌ Refresh failed: {result['error']}")
        
        # Reset confirmation state on page load
        if 'confirm_reset' not in st.session_state:
            st.session_state.confirm_reset = False
    
    # Main content area
    if mode == "chat":
        chat_interface(bot)
    elif mode == "quiz":
        quiz_interface(bot)
    elif mode == "summary":
        summary_interface(bot)
    elif mode == "documents":
        documents_interface(bot)

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

def documents_interface(bot: StudyMateBot):
    """Comprehensive Documents Management Interface"""
    st.header("📁 Document Management Center")
    
    # Quick stats
    with st.spinner("Loading document statistics..."):
        stats = bot.get_store_stats()
        docs_list = bot.list_documents()
    
    if "error" not in stats and "error" not in docs_list:
        # Statistics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Total Documents", stats.get('total_documents', 0))
        
        with col2:
            st.metric("📁 Unique Files", stats.get('unique_files', 0))
        
        with col3:
            st.metric("🧩 Total Chunks", docs_list.get('total_chunks', 0))
        
        with col4:
            db_type = stats.get('vector_db_type', 'Unknown').upper()
            st.metric("🗄️ Database", db_type)
        
        # File types breakdown
        if stats.get('file_types'):
            st.subheader("📊 Document Types")
            file_types = stats['file_types']
            
            cols = st.columns(len(file_types))
            for i, (file_type, count) in enumerate(file_types.items()):
                with cols[i]:
                    st.metric(f"{file_type.upper()}", count)
        
        st.divider()
        
        # Document Browser
        st.subheader("🗂️ Document Browser")
        
        if docs_list.get('documents'):
            # Search and filter
            col1, col2 = st.columns([3, 1])
            
            with col1:
                search_term = st.text_input("🔍 Search documents", placeholder="Type filename to search...")
            
            with col2:
                file_type_filter = st.selectbox("📄 Filter by type", ["All"] + list(stats.get('file_types', {}).keys()))
            
            # Filter documents
            filtered_docs = docs_list['documents']
            
            if search_term:
                filtered_docs = [doc for doc in filtered_docs if search_term.lower() in doc['filename'].lower()]
            
            if file_type_filter != "All":
                filtered_docs = [doc for doc in filtered_docs if doc['file_type'] == file_type_filter]
            
            st.write(f"**Showing {len(filtered_docs)} of {len(docs_list['documents'])} documents**")
            
            # Document cards
            for doc in filtered_docs:
                with st.container():
                    col1, col2, col3 = st.columns([4, 1, 2])
                    
                    with col1:
                        st.write(f"📄 **{doc['filename']}**")
                        st.caption(f"ID: `{doc['document_id'][:12]}...`")
                    
                    with col2:
                        st.write(f"**{doc['file_type']}**")
                        st.caption(f"{doc['chunks_found']} chunks")
                    
                    with col3:
                        # Individual document actions
                        if st.button(f"🔍 Preview", key=f"preview_{doc['document_id']}"):
                            # Show document preview
                            with st.expander(f"Preview: {doc['filename']}", expanded=True):
                                # Try to get a sample from the document
                                sample_response = bot.ask_question(f"What is the main topic of {doc['filename']}?")
                                if "error" not in sample_response and sample_response.get('sources'):
                                    source_content = sample_response['sources'][0]['content']
                                    st.write("**Sample content:**")
                                    st.text_area("Content preview", source_content[:500] + "..." if len(source_content) > 500 else source_content, height=100)
                                else:
                                    st.info("Unable to load preview")
                        
                        if st.button(f"❌ Remove", key=f"remove_{doc['document_id']}"):
                            # Individual document removal
                            with st.spinner(f"Removing {doc['filename']}..."):
                                result = bot.remove_specific_documents([doc['document_id']])
                                if "error" not in result:
                                    st.success(f"✅ Removed {doc['filename']}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Failed to remove: {result['error']}")
                    
                    st.divider()
        else:
            # Empty state
            st.info("📭 No documents found")
            st.markdown("""
            **Get started:**
            1. Use the sidebar to upload documents
            2. Or drag and drop files in the bulk upload section
            3. Switch to Chat mode to start asking questions
            """)
        
        st.divider()
        
        # Bulk Operations
        st.subheader("⚡ Bulk Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh All", help="Reload documents from data folder", use_container_width=True):
                with st.spinner("Refreshing documents..."):
                    result = bot.replace_all_documents()
                    if "error" not in result:
                        st.success(f"✅ Refreshed! {result.get('unique_documents', 0)} documents loaded")
                        st.rerun()
                    else:
                        st.error(f"❌ Refresh failed: {result['error']}")
        
        with col2:
            if st.button("🧹 Clear All", help="Remove all documents from memory", use_container_width=True):
                if st.session_state.get('confirm_clear_all', False):
                    with st.spinner("Clearing all documents..."):
                        result = bot.clear_all_documents()
                        if "error" not in result:
                            st.success("✅ All documents cleared!")
                            st.session_state.confirm_clear_all = False
                            st.rerun()
                        else:
                            st.error(f"❌ Clear failed: {result['error']}")
                else:
                    st.session_state.confirm_clear_all = True
                    st.warning("⚠️ Click again to confirm clearing all documents")
                    st.rerun()
        
        with col3:
            if st.button("💾 Create Backup", help="Create backup of current documents", use_container_width=True):
                with st.spinner("Creating backup..."):
                    result = bot.create_backup()
                    if "error" not in result:
                        backup_name = result.get('backup_name', 'Unknown')
                        st.success(f"✅ Backup created: {backup_name}")
                    else:
                        st.error(f"❌ Backup failed: {result['error']}")
        
        # Memory Health Check
        st.subheader("🩺 Memory Health Check")
        
        if st.button("🧪 Test Memory", help="Test if old content has been properly cleared"):
            with st.spinner("Testing memory for old content..."):
                test_result = bot.test_memory_reset()
                
                if test_result.get("memory_clean", True):
                    st.success("✅ Memory is clean - no residual content detected!")
                else:
                    st.warning("⚠️ Some old content may still be present")
                    
                    with st.expander("🔍 Test Details"):
                        for test in test_result.get("queries_tested", []):
                            status = "✅" if test.get("is_clean", False) else "⚠️"
                            st.write(f"{status} **'{test['query']}'**: {'Clean' if test.get('is_clean', False) else 'Has residual content'}")
        
        # Reset confirmation state
        if 'confirm_clear_all' not in st.session_state:
            st.session_state.confirm_clear_all = False
            
    else:
        st.error("❌ Unable to load document statistics")
        
        # Fallback options
        st.subheader("🔧 Basic Operations")
        
        if st.button("🔄 Try Refresh"):
            with st.spinner("Attempting document refresh..."):
                result = bot.replace_all_documents()
                if "error" not in result:
                    st.success("✅ Refresh successful!")
                    st.rerun()
                else:
                    st.error(f"❌ Refresh failed: {result['error']}")

if __name__ == "__main__":
    main()
