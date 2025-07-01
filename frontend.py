import streamlit as st
from System.helper import (get_pdf_text ,
                            load_model ,
                              text_splitter , 
                              get_conversational_chain , 
                              user_query ,
                                vector_Store)

# Configure page
def main():
    st.set_page_config(
        page_title="AI PDF Assistant", 
        page_icon="🤖", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS styling
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .main > div {
            padding-top: 2rem;
        }
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom Header */
        .app-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .app-title {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .app-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 400;
        }
        
        /* Chat Container */
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }
        
        /* Chat Messages */
        .chat-message {
            display: flex;
            margin-bottom: 1.5rem;
            padding: 1rem;
            border-radius: 18px;
            animation: fadeIn 0.3s ease-in;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .chat-message.user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: 20%;
            justify-content: flex-end;
        }
        
        .chat-message.bot {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin-right: 20%;
            justify-content: flex-start;
        }
        
        .chat-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            margin: 0 12px;
            border: 3px solid rgba(255,255,255,0.3);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .chat-content {
            flex: 1;
            font-size: 0.95rem;
            line-height: 1.6;
            font-weight: 400;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* Upload Area */
        .upload-area {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .upload-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .upload-subtitle {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Clear Button Special Styling */
        .clear-btn {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
        }
        
        /* Input Field */
        .stChatInput > div > div > input {
            border-radius: 25px;
            border: 2px solid #e2e8f0;
            padding: 0.8rem 1.2rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            background: white;
        }
        
        .stChatInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* File Upload */
        .stFileUploader > div > div {
            background: white;
            border: 2px dashed #cbd5e0;
            border-radius: 15px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader > div > div:hover {
            border-color: #667eea;
            background: #f7fafc;
        }
        
        /* Success/Info Messages */
        .stSuccess, .stInfo {
            border-radius: 12px;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Developer Info */
        .developer-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            margin-top: 2rem;
        }
        
        .developer-name {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .developer-title {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .developer-link {
            color: white;
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .developer-link:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        /* Status Indicators */
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-ready {
            background-color: #10b981;
            animation: pulse 2s infinite;
        }
        
        .status-processing {
            background-color: #f59e0b;
            animation: pulse 1s infinite;
        }
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .chat-message.user {
                margin-left: 5%;
            }
            .chat-message.bot {
                margin-right: 5%;
            }
            .app-title {
                font-size: 2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # App Header
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">🤖 AI PDF Assistant</h1>
            <p class="app-subtitle">Intelligent document analysis and conversation</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "processing_status" not in st.session_state:
        st.session_state.processing_status = "ready"

    # Status indicator
    status_class = "status-ready" if st.session_state.processing_status == "ready" else "status-processing"
    status_text = "Ready to chat" if st.session_state.processing_status == "ready" else "Processing documents..."
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem; color: #64748b;">
            <span class="status-indicator {status_class}"></span>
            {status_text}
        </div>
    """, unsafe_allow_html=True)
    
    # Chat input (outside of columns)
    user_question = st.chat_input("💬 Ask me anything about your documents...")
    
    if user_question:
        if st.session_state.processing_status == "ready":
            with st.spinner("🤔 Thinking..."):
                response = user_query(user_question)
                st.session_state.history.append({"role": "user", "message": user_question})
                st.session_state.history.append({"role": "bot", "message": response})
                st.rerun()
        else:
            st.warning("⏳ Please wait for document processing to complete before asking questions.")

    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Clear chat button
        col_clear, col_empty = st.columns([1, 4])
        with col_clear:
            if st.button("🧹 Clear Chat", key="clear_chat"):
                st.session_state.history = []
                st.rerun()
        
        # Display chat history
        chat_placeholder = st.container()
        with chat_placeholder:
            if not st.session_state.history:
                st.markdown("""
                    <div style="text-align: center; padding: 3rem; color: #64748b;">
                        <h3>👋 Welcome!</h3>
                        <p>Upload your PDF documents and start chatting to get insights, summaries, and answers.</p>
                        <div style="margin-top: 2rem;">
                            <div style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; background: #f1f5f9; border-radius: 20px; font-size: 0.9rem;">
                                📄 Document Analysis
                            </div>
                            <div style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; background: #f1f5f9; border-radius: 20px; font-size: 0.9rem;">
                                🔍 Smart Search
                            </div>
                            <div style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; background: #f1f5f9; border-radius: 20px; font-size: 0.9rem;">
                                💡 Q&A Assistant
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                for i, chat in enumerate(st.session_state.history):
                    if chat["role"] == "user":
                        st.markdown(f'''
                            <div class="chat-message user">
                                <div class="chat-content">{chat["message"]}</div>
                                <img class="chat-avatar" src="https://cdn-icons-png.freepik.com/512/6596/6596121.png" alt="User"/>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="chat-message bot">
                                <img class="chat-avatar" src="https://img.freepik.com/free-vector/graident-ai-robot-vectorart_78370-4114.jpg" alt="AI Assistant"/>
                                <div class="chat-content">{chat["message"]}</div>
                            </div>
                        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div class="upload-area">
                <div class="upload-title">📁 Document Upload</div>
                <div class="upload-subtitle">Upload your PDF files to get started</div>
            </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        doc_files = st.file_uploader(
            label="Choose PDF files",
            accept_multiple_files=True,
            type=['pdf'],
            help="You can upload multiple PDF files at once. Maximum file size: 200MB per file."
        )
        
        # Display uploaded files
        if doc_files:
            st.markdown("**📋 Uploaded Files:**")
            for i, file in enumerate(doc_files, 1):
                file_size = len(file.getvalue()) / (1024*1024)  # Size in MB
                st.markdown(f"• {file.name} ({file_size:.1f} MB)")
        
        # Process button
        if st.button("🚀 Process Documents", disabled=not doc_files):
            if doc_files:
                st.session_state.processing_status = "processing"
                with st.spinner("🔄 Processing your documents..."):
                    try:
                        raw_text = get_pdf_text(doc_files)
                        text_chunks = text_splitter(raw_text)
                        vector_Store(text_chunks)
                        st.session_state.processing_status = "ready"
                        st.success("✅ Documents processed successfully!")
                        st.balloons()
                    except Exception as e:
                        st.session_state.processing_status = "ready"
                        st.error(f"❌ Error processing documents: {str(e)}")
            else:
                st.warning("⚠️ Please upload PDF files first.")
        
        # Stats section
        if st.session_state.history:
            st.markdown("---")
            st.markdown("**📊 Chat Statistics**")
            user_messages = len([msg for msg in st.session_state.history if msg["role"] == "user"])
            bot_messages = len([msg for msg in st.session_state.history if msg["role"] == "bot"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Questions", user_messages)
            with col2:
                st.metric("Responses", bot_messages)
        
        # Developer info
        st.markdown("---")
        st.markdown("""
            <div class="developer-card">
                <div class="developer-name">Sayed Ali Elsayed</div>
                <div class="developer-title">AI Engineer | ML Specialist</div>
                <div style="margin-bottom: 1rem; font-size: 0.85rem; opacity: 0.9;">
                    Passionate about machine learning, NLP, and creating intelligent solutions
                </div>
                <a href="https://www.linkedin.com/in/sayed-ali-482668262/" class="developer-link" target="_blank">
                    🔗 Connect on LinkedIn
                </a>
                <div style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;">
                    © 2025 Sayed Ali Elsayed
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()