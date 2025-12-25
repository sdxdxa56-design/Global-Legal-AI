import streamlit as st
import json
from langchain_community.tools import DuckDuckGoSearchRun

# --- 1. إعدادات الصفحة والتمويه لإخفاء أثر Streamlit ---
st.set_page_config(page_title="المحامي الدولي الذكي", layout="wide")

st.markdown("""
    <style>
    /* إخفاء القوائم والشعارات ليكون الموقع مستقلاً */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #stDecoration {display:none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    
    /* تصميم الواجهة السوداء ChatGPT Style */
    .stApp { background-color: #0d1117; color: white; }
    .stChatInput { border-radius: 25px !important; border: 1px solid #30363d !important; }
    .stChatMessage { border-radius: 15px !important; background-color: #161b22 !important; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البحث والتدريب التلقائي ---
def lawyer_engine(query):
    try:
        # المحرك يبحث تلقائياً في الإنترنت عن القوانين الدولية
        search = DuckDuckGoSearchRun()
        search_query = f"site:un.org OR site:interpol.int قانون جنائي ومرافعات {query}"
        return search.run(search_query)
    except Exception as e:
        return "عذراً، جاري تحديث الاتصال بقواعد البيانات القانونية الدولية. يرجى المحاولة مرة أخرى."

# --- 3. واجهة المستخدم ---
st.title("⚖️ المحامي الدولي الذكي")
st.write("خبير التحليل الجنائي، صياغة المرافعات، وفحص الوثائق")

# نظام الذاكرة للمحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال من المستخدم
if prompt := st.chat_input("اطرح قضيتك أو استفسارك القانوني هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري تحليل القضية والبحث في القوانين الدولية..."):
            response = lawyer_engine(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 4. بوابة الـ API للربط بالمشاريع الأخرى ---
# المفتاح الخاص بك: LEGAL_AI_2024_PROTECT
if st.query_params.get("api") == "true" and st.query_params.get("key") == "LEGAL_AI_2024_PROTECT":
    st.write(json.dumps({"status": "active", "engine": "Global_Legal_v1"}))
    st.stop()
