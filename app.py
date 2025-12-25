import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
import json

# --- 1. إخفاء هوية Streamlit تماماً (CSS سحري) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #stDecoration {display:none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    /* تصميم يشبه ChatGPT */
    .stApp { background-color: #0d1117; color: white; }
    .stChatInput { border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام الصلاحيات (مطور vs مستخدم) ---
# يمكنك الدخول كمطور بإضافة ?role=admin للرابط
params = st.query_params
is_admin = params.get("role") == "admin"

# --- 3. محرك التدريب التلقائي (البحث الحي) ---
search = DuckDuckGoSearchRun()

def legal_ai_engine(query):
    # هنا المحامي يبحث تلقائياً في الإنترنت عن القوانين
    with st.spinner("جاري فحص القوانين الدولية والمرافعات..."):
        context = search.run(f"site:un.org OR site:interpol.int قانون جنائي ومرافعات {query}")
        return context

# --- 4. الواجهة الأمامية ---
st.title("⚖️ المحامي الدولي الذكي")
st.caption("نظام قانوني جنائي مستقل ومستشار دولي")

# إظهار شريط الإعدادات للمطور فقط
if is_admin:
    with st.sidebar:
        st.header("🛠 لوحة المطور")
        st.write("المفتاح الخاص بك: `LEGAL_AI_2024_PROTECT`")
        if st.button("تفريغ الذاكرة التلقائية"):
            st.success("تم مسح البيانات المؤقتة")

# نظام الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل المحامي الذكي عن قضيتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # الرد المعتمد على البحث التلقائي
    legal_response = legal_ai_engine(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(f"**التحليل القانوني التلقائي:**\n\n{legal_response}")
    st.session_state.messages.append({"role": "assistant", "content": legal_response})

# --- 5. نظام الـ Webhook المدمج ---
if "api" in params and params.get("key") == "LEGAL_AI_2024_PROTECT":
    st.write(json.dumps({"status": "connected", "engine": "Auto-Train Active"}))
    st.stop()
