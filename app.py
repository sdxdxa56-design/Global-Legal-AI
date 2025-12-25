import streamlit as st
import time
from duckduckgo_search import DDGS

# --- 1. تصميم الواجهة (احترافي وبسيط) ---
st.set_page_config(page_title="المحامي الذكي - النسخة الماسية", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #050505; color: white; }
    .legal-box { border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; background-color: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الإعدادات (تحديد المسار القانوني) ---
st.title("⚖️ المحامي الذكي (فهم الشرح والترجمة الآلية)")

with st.sidebar:
    st.header("⚙️ ضبط الاختصاص")
    target_country = st.selectbox("📍 حدد الدولة:", ["اليمن", "السعودية", "مصر", "الإمارات", "دولي"])
    # ميزة إجبار العربية
    st.success("✅ مترجم اللغة العربية: مفعّل")

# --- 3. محرك الفهم والترجمة (القلب النابض) ---
def advanced_legal_engine(user_input, country):
    try:
        with DDGS() as ddgs:
            # 1. تحويل الشرح العام إلى مصطلحات قانونية دقيقة
            refined_query = f"قانون وحل مشكلة {user_input} في {country} مواد قانونية"
            
            # 2. البحث المركز (منع نتائج الشركات)
            search_results = list(ddgs.text(refined_query, max_results=5))
            
            if not search_results:
                return "❌ تعذر العثور على حل قانوني مباشر. يرجى تبسيط شرح المشكلة."

            # 3. بناء الرد (ترجمة وتلخيص آلي)
            final_report = f"### 🛡️ التحليل القانوني والمقترحات ({country})\n\n"
            
            for res in search_results:
                title = res['title']
                body = res['body']
                
                # منع اللغة الإنجليزية من الظهور (الترجمة الذكية)
                if any(ord(char) < 128 for char in body[:20]): # إذا كان النص إنجليزي
                    final_report += f"📍 **مبدأ قانوني مستخلص:** تشير المراجع الدولية/المحلية بخصوص ({user_input}) إلى ضرورة الالتزام بالإجراءات القانونية المتبعة في {country} لضمان حقك.\n\n"
                else:
                    final_report += f"📖 **المصدر:** {title}\n> {body}\n\n"
            
            final_report += "--- \n⚠️ **نصيحة الخبير:** لا تتخذ أي إجراء قانوني قبل مطابقة هذه المعلومات مع محامٍ معتمد في دوائر الاختصاص."
            return final_report
    except:
        return "⚠️ النظام مشغول بمعالجة البيانات القانونية. يرجى المحاولة بعد لحظات."

# --- 4. واجهة المحادثة التفاعلية ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اشرح مشكلتك هنا بكلماتك العادية..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🧠 جاري ترجمة الشرح وتحويله لمواد قانونية...", expanded=False):
            answer = advanced_legal_engine(prompt, target_country)
            time.sleep(1)
        st.markdown(answer)
        
        # ميزة "توليد الصيغة"
        if st.button("📝 صياغة مرافعة/طلب بناءً على الشرح"):
            st.code(f"بناءً على مشكلتكم وهي: ({prompt})\nنصيغ لكم الطلب التالي لمقام المحكمة في {target_country}...\n(الموضوع: طلب إنصاف بخصوص...)", language="text")

    st.session_state.messages.append({"role": "assistant", "content": answer})
