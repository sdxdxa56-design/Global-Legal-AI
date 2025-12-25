import streamlit as st

# إعدادات الصفحة (تصميم يشبه ChatGPT)
st.set_page_config(page_title="المحامي الذكي العالمي", layout="centered")

st.title("⚖️ المحامي الدولي الذكي")
st.markdown("تحليل قانوني، كشف تزوير، ومرافعات جنائية")

# قائمة جانبية لرفع الملفات (عقود، تقارير، صور)
with st.sidebar:
    st.header("المستندات القانونية")
    uploaded_file = st.file_uploader("ارفع وثيقة لفحصها (PDF, TXT, Image)", type=['pdf', 'txt', 'jpg', 'png'])
    if uploaded_file:
        st.success("تم رفع الملف بنجاح، جاري التحليل...")

# بناء واجهة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل عن قضية أو اطلب مرافعة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # هنا سيتم لاحقاً ربط "مخ" الذكاء الاصطناعي
    response = f"جاري تحليل القضية بناءً على القوانين الدولية... (رد تجريبي)"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
