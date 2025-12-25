import streamlit as st
import time
import pycountry
from duckduckgo_search import DDGS
from langdetect import detect

# =====================
# إعدادات الصفحة
# =====================
st.set_page_config(
    page_title="⚖️ Global Legal AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# CSS
# =====================
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp { background-color: #0b0b0b; color: #ffffff; }
.stChatInput { border: 2px solid #00ffd5; border-radius: 20px; }
.box { background:#111; border:1px solid #00ffd5; padding:15px; border-radius:10px; }
.icon { font-size:20px; }
</style>
""", unsafe_allow_html=True)

# =====================
# العنوان
# =====================
st.title("⚖️ المحامي العالمي الذكي")
st.caption("نظام قانوني يفهم مشكلتك كما تشرحها – لا كما تُعنونها")

# =====================
# الشريط الجانبي
# =====================
with st.sidebar:
    st.header("⚙️ الإعدادات القانونية")

    # اللغة
    response_lang = st.radio(
        "🌐 لغة الرد",
        ["العربية", "English"],
        horizontal=True
    )

    # الدولة
    countries = sorted([c.name for c in pycountry.countries])
    selected_country = st.selectbox("📍 الدولة المطبقة", countries)

    # نوع القضية
    case_type = st.selectbox(
        "⚖️ نوع القضية",
        ["شخصية / مدنية", "جنائية", "إدارية", "دولية"]
    )

    # المؤسسة
    institution = st.radio(
        "🏛️ الجهة المختصة",
        [
            "🏠 محكمة محلية",
            "⚖️ محكمة دستورية",
            "🌍 محكمة دولية",
            "🛂 الإنتربول",
            "🕊️ حقوق الإنسان"
        ]
    )

    st.divider()
    conservative_mode = st.toggle("🧠 وضع المحامي المحافظ", value=True)

# =====================
# محرك الفهم الذكي
# =====================
def detect_intent(text):
    keywords_criminal = ["قتل", "سرقة", "جريمة", "اعتداء", "سجن"]
    keywords_personal = ["طلاق", "نفقة", "أرض", "إيجار", "ورثة"]

    for k in keywords_criminal:
        if k in text:
            return "جنائية"
    for k in keywords_personal:
        if k in text:
            return "مدنية"

    return "غير محدد"

# =====================
# محرك القانون
# =====================
def legal_engine(text, country, case_type, lang):
    with DDGS() as ddgs:
        query = f"{text} قانون {country}"
        results = list(ddgs.text(query, max_results=3))

    if not results:
        return "❌ لم يتم العثور على أساس قانوني واضح. حاول تبسيط الوصف."

    response = ""
    if lang == "العربية":
        response += f"### 📜 التحليل القانوني ({country})\n"
        response += f"**الوصف:** {text}\n\n"
        for r in results:
            response += f"📌 **قاعدة قانونية محتملة:**\n{r['body']}\n\n"
    else:
        response += f"### Legal Analysis ({country})\n"
        response += f"Case description: {text}\n\n"
        for r in results:
            response += f"- Legal reference:\n{r['body']}\n\n"

    return response

# =====================
# المحادثة
# =====================
if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("اشرح مشكلتك القانونية بأي أسلوب...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    intent = detect_intent(user_input)

    # منع الخلط
    if intent != "غير محدد" and intent not in case_type:
        warning = "⚠️ تنبيه: وصفك يشير إلى نوع قضية مختلف عن المحدد."
        st.warning(warning)

    with st.chat_message("assistant"):
        with st.status("🧠 تحليل قانوني جارٍ...", expanded=False):
            time.sleep(1)
            answer = legal_engine(
                user_input,
                selected_country,
                case_type,
                response_lang
            )
        st.markdown(answer)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 توليد مرافعة رسمية"):
                st.code(
                    f"إلى المحكمة المختصة في {selected_country}\n"
                    f"الموضوع: {user_input}\n"
                    f"نلتمس عدالتكم النظر في هذه الوقائع..."
                )

        with col2:
            if st.button("🔍 تصحيح التحليل"):
                st.info("سيتم إعادة التحليل مع تشديد المعايير القانونية.")

    st.session_state.chat.append({"role": "assistant", "content": answer})
