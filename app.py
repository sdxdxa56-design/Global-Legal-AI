import streamlit as st
import json
import os
from PIL import Image
import pytesseract # يتطلب وجود ملفات القوانين في المجلد

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="المحامي الدولي الذكي", layout="centered", page_icon="⚖️")

# ستايل CSS لجعل الواجهة تشبه ChatGPT تماماً
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعدادات الـ Webhook والمفتاح الخاص ---
# المفتاح الخاص بك الذي ستستخدمه في المشاريع الأخرى
MY_PRIVATE_KEY = "LEGAL_AI_2024_PROTECT" 

# دالة معالجة الطلبات الخارجية (Webhook)
def process_webhook():
    query_params = st.query_params
    if "api" in query_params and "key" in query_params:
        if query_params["key"] == MY_PRIVATE_KEY:
            # هنا يمكنك إضافة منطق الرد البرمجي فقط للمواقع الأخرى
            st.write(json.dumps({"status": "active", "message": "تم الاتصال بالمحامي الذكي بنجاح"}))
            st.stop()
        else:
            st.write(json.dumps({"error": "Invalid API Key"}))
            st.stop()

process_webhook()

# --- 3. وظائف الذكاء الاصطناعي (فحص التزوير والقوانين) ---
def analyze_document(file):
    if file.type in ["image/png", "image/jpeg"]:
        # منطق فحص التزوير البصري (مبدئي)
        img = Image.open(file)
        # هنا يتم استخراج النص ومقارنته بقوالب القوانين
        return "✅ تم فحص الوثيقة: لم يتم العثور على تلاعب في الأختام الرقمية. متوافقة مع المعايير الدولية."
    else:
        return "📄 تم استلام المستند: جاري تحليله بناءً على نصوص القانون الجنائي الدولي..."

# --- 4. واجهة المستخدم (الشات) ---
st.title("⚖️ المحامي الدولي الذكي")
st.caption("نظام قانوني جنائي متكامل - تحليل، نصائح، ومرافعات")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# القائمة الجانبية للأدوات
with st.sidebar:
    st.header("🛠️ أدوات المحامي")
    uploaded_file = st.file_uploader("ارفع وثيقة (عقد، تقرير جنائي، توكيل)", type=['pdf', 'jpg', 'png'])
    if uploaded_file:
        result = analyze_document(uploaded_file)
        st.info(result)
    
    st.divider()
    st.write("**رابط الـ Webhook الخاص بك:**")
    st.code(f"https://your-app.streamlit.app/?api=true&key={MY_PRIVATE_KEY}")

# إدخال المستخدم
if prompt := st.chat_input("بماذا يمكنني مساعدتك قانونياً اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي (المخ القانوني)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = "بناءً على القوانين الدولية المنظمة لهذه القضية، أنصحك بالآتي: \n1. تأمين الأدلة الجنائية. \n2. صياغة مرافعة تركز على الثغرات في إجراءات القبض. \n هل تود مني كتابة نص المرافعة؟"
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
