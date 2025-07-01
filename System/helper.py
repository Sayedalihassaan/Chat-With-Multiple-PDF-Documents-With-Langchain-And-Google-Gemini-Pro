from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st




load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



def load_model(name_model="gemini-1.5-flash") :
    llm = ChatGoogleGenerativeAI(
        model = name_model , 
        google_api_key=GOOGLE_API_KEY
    )

    return llm 

model = load_model(name_model="gemini-1.5-flash")


def get_pdf_text(data_path):
    text = ""
    if not isinstance(data_path, list):
        data_path = [data_path]

    for i in data_path:
        if i is not None:
            pdf = PdfReader(i)
            for j in pdf.pages:
                text += j.extract_text()
    return text



def text_splitter(text) :
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 5000 , chunk_overlap = 200)
    chunk = text_splitter.split_text(text = text)

    return chunk


embedding = None
def vector_Store(text_split) :

    global embedding
    embedding = GoogleGenerativeAIEmbeddings(
        model = "models/embedding-001" , 
        google_api_key = GOOGLE_API_KEY , 

    )
    vector_Store = FAISS.from_texts(text_split , embedding)
    vector_Store.save_local(folder_path = "faiss-index")



def get_conversational_chain() :
    prompt_template = """You are a knowledgeable and professional AI assistant specializing in providing accurate information from the given context.
                         Your role is to:\n\n"
                         "1. Provide clear, concise, and accurate answers based on the provided context and conversation history\n"
                         "2. If the context doesn't contain enough information to fully answer a question, acknowledge this limitation\n"
                         "3. Maintain a professional and helpful tone while ensuring factual accuracy\n"
                         "4. Use direct quotes from the context when relevant to support your answers\n"
                         "5. Organize complex responses in a structured, easy-to-read format\n"
                         "6. Consider the previous conversation history to maintain context and provide coherent responses\n"
                         "7. If you need to make assumptions, explicitly state them\n\n"
                         "Remember:\n"
                         "- Stay within the scope of the provided context\n"
                         "- Use conversation history to better understand the context of questions\n"
                         "- Avoid making up information or speculating beyond the given content\n"
                         "- If multiple interpretations are possible, present them clearly\n"
                         "- Maintain consistency in your responses\n\n"
                         "Previous conversation history:\n{history}\n\n"
                         "Context from documents:\n{context}\n\n"
                         "Question: {input}\n\n"
                         "Answer: 
                         """
    
    model = load_model()
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "input", "history"])
    chain = load_qa_chain(llm = model , chain_type = "stuff" , prompt=prompt)
    return chain




def user_query(question) :

    global embedding
    if embedding is None:
        # Recreate the embedding model if it doesn't exist
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
    

    db = FAISS.load_local(
        folder_path="faiss-index", 
        embeddings=embedding,
        allow_dangerous_deserialization=True
    )
    
    docs = db.similarity_search(query=question, k=10)

    chain = get_conversational_chain()


    history = ""
    if "history" in st.session_state:
        for chat in st.session_state.history[-5:]:  
            role = "User" if chat["role"] == "user" else "Assistant"
            history += f"{role}: {chat['message']}\n"

    chain_input = {
        "input_documents": docs,
        "input": question,
        "history": history
    }
    
    response = chain(
        chain_input,
        return_only_outputs=True
    )
    return response["output_text"]