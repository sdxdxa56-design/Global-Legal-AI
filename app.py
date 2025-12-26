import streamlit as st
import time
from duckduckgo_search import DDGS
from datetime import datetime

# --- 1. إعدادات المظهر الفخم (نفس نمطك مع تحسينات) ---
st.set_page_config(page_title="المحامي الماسي - العقل التفاعلي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .stApp { background-color: #0d1117; color: white; }
    .chat-bubble-ai { 
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
        padding: 20px; border-radius: 15px; border-right: 5px solid #00ffcc; margin: 10px 0;
    }
    .urgent-box { 
        background: linear-gradient(135deg, #991b1b 0%, #ef4444 100%); 
        padding: 15px; border-radius: 10px; font-weight: bold; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.7;} 100% {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

# --- 2. عقل المحامي (التحليل الذكي والرد التفاعلي) ---
def advanced_legal_brain(user_input, country):
    # التحليل الأولي للمشاعر والنية
    is_crime_confession = any(word in user_input for word in ["قتلت", "سرقت", "ضربت", "جريمة"])
    
    response_data = {
        "logic_advice": "",
        "legal_articles": [],
        "steps": []
    }

    # منطق ChatGPT للتفاعل مع المواقف الخطيرة
    if is_crime_confession:
        response_data["logic_advice"] = f"""
        🛑 **تحليل الموقف (سري وهام):** لقد ذكرت أمراً في غاية الخطورة. بصفتي مساعدك الذكي، أذكرك أن قوانين **{country}** تأخذ هذه الاعترافات بمحمل الجد. 
        **نصيحة فورية:** توقف عن الحديث عن التفاصيل لأي شخص، وابحث عن محامٍ فوراً. تسليم النفس في بعض الحالات قد يخفف العقوبة، لكن لا تفعل ذلك دون استشارة قانونية رسمية.
        """
    else:
        response_data["logic_advice"] = f"💡 **تحليل الخبير:** بناءً على وصفك لمشكلة '{user_input}' في {country}، إليك المسار القانوني الصحيح:"

    # البحث الأوتوماتيكي عن القوانين (التغذية الراجعة)
    try:
        with DDGS() as ddgs:
            search_query = f"عقوبة وإجراءات {user_input} في قانون {country}"
            results = list(ddgs.text(search_query, max_results=3))
            for r in results:
                response_data["legal_articles"].append(r['body'])
    except:
        response_data["legal_articles"].append("تعذر جلب النصوص القانونية اللحظية، يرجى مراجعة دستور الدولة.")

    return response_data

# --- 3. واجهة المستخدم ---
st.title("⚖️ المحامي الماسي (الذكاء التفاعلي)")
st.caption("أنا لا أبحث فقط، أنا أفهم وأحلل وأعطيك نصيحة كشخص حقيقي.")

with st.sidebar:
    st.header("⚙️ الضبط")
    country = st.selectbox("📍 الدولة:", ["اليمن", "السعودية", "مصر", "الإمارات", "دولي"])
    st.divider()
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.messages = []
        st.rerun()

# إدارة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اشرح موقفك الآن (مثال: أنا قتلت شخص بالخطأ ماذا أفعل؟)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🧠 العقل الاصطناعي يحلل الموقف قانونياً ومنطقياً...", expanded=False):
            result = advanced_legal_brain(prompt, country)
            time.sleep(1.5)
        
        # بناء الرد النهائي بأسلوب ChatGPT
        full_res = f"<div class='chat-bubble-ai'>{result['logic_advice']}</div>"
        
        if result['legal_articles']:
            full_res += "### 📖 السند القانوني الذي وجدته لك:\n"
            for art in result['legal_articles']:
                full_res += f"> {art}\n\n"
        
        st.markdown(full_res, unsafe_allow_html=True)
        
        # أزرار الطوارئ التفاعلية
        if "قتلت" in prompt or "جريمة" in prompt:
            st.markdown("<div class='urgent-alert'>⚠️ هل تود استخراج أقرب مكتب محاماة جنائي الآن؟</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_res})
