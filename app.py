import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json

# --- 1. إعدادات النظام ---
MY_PRIVATE_KEY = "LEGAL_AI_2024_PROTECT"
DB_PATH = "vectorstore/db_faiss"

# --- 2. محرك التدريب والقراءة (RAG) ---
def create_knowledge_base():
    if not os.path.exists('knowledge_base'):
        os.makedirs('knowledge_base')
        return None
    
    # تحميل القوانين من المجلد
    loader = DirectoryLoader('knowledge_base', glob='./*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        return None

    # تحويل النصوص إلى أرقام (Embeddings) ليفهمها الذكاء الاصطناعي
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(DB_PATH)
    return db

# --- 3. واجهة المستخدم والتصميم ---
st.set_page_config(page_title="المحامي الذكي", layout="wide")
st.title("⚖️ منصة المحاماة الجنائية الدولية")

# تفعيل التدريب عند وجود ملفات جديدة
if st.sidebar.button("تحديث قاعدة البيانات القانونية"):
    with st.spinner("جاري قراءة القوانين وتدريب المحرك..."):
        db = create_knowledge_base()
        if db: st.success("تم تحديث معلومات المحامي بنجاح!")
        else: st.error("لم يتم العثور على ملفات PDF في مجلد knowledge_base")

# --- 4. منطق الرد والتحليل ---
def get_legal_advice(user_query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    try:
        # البحث في القوانين المخزنة
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        docs = db.similarity_search(user_query)
        context = "\n".join([doc.page_content for doc in docs])
        return f"بناءً على نصوص القوانين المتوفرة لدي:\n\n{context[:1000]}..." 
    except:
        return "أنا جاهز، ولكن يرجى رفع ملفات القوانين في مجلد knowledge_base أولاً ثم الضغط على تحديث."

# --- 5. نظام الشات والـ Webhook ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عن ثغرة قانونية أو حل لقضية جنائية..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_legal_advice(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
