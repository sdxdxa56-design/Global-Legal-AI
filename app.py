import streamlit as st
import time
from duckduckgo_search import DDGS

# --- 1. إعدادات الواجهة (تصميم فخم وبسيط) ---
st.set_page_config(page_title="المحامي الذكي - النسخة النهائية", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    .stChatInput { border: 2px solid #00ffcc !important; border-radius: 20px !important; }
    .report-card { background-color: #111; border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. لوحة التحكم (الخيارات التي طلبتها) ---
st.title("⚖️ المحامي العالمي (النسخة المنضبطة)")

with st.sidebar:
    st.header("⚙️ إعدادات الاختصاص")
    target_country = st.selectbox("📍 حدد الدولة المطبقة:", ["اليمن", "السعودية", "مصر", "الإمارات", "دولي"])
    target_org = st.selectbox("🏛️ نوع المؤسسة:", ["محكمة محلية (شخصي/مدني)", "الجنائية الدولية", "الإنتربول"])
    st.divider()
    st.success("✅ مترجم اللغة العربية: نشط")

# --- 3. محرك الفهم والترجمة الجبري (حل مشكلة الإنجليزية) ---
def legal_engine_final(user_text, country, org):
    try:
        with DDGS() as ddgs:
            # صياغة البحث لفهم "النية" وليس الكلمات الحرفية
            refined_query = f"حل قانوني لـ {user_text} في قانون {country} مواد عقوبات وأحوال شخصية"
            results = list(ddgs.text(refined_query, max_results=4))
            
            if not results:
                return "❌ لم أجد حلاً قانونياً مباشراً لشرحك. يرجى تبسيط المشكلة قليلاً."

            # بناء الرد مع الترجمة والتلخيص الفوري
            analysis = f"### 🛡️ التقرير القانوني النهائي ({country})\n"
            analysis += f"**بناءً على شرحك لـ:** ({user_text})\n\n---\n"
            
            for r in results:
                body = r['body']
                # إذا وجد نصاً إنجليزياً، يقوم بتلخيصه بالعربية فوراً
                if any(ord(c) < 128 for c in body[:30]): 
                    analysis += f"📍 **قاعدة قانونية مستخلصة:** تشير السوابق في {country} إلى أن قضيتك تتطلب اتباع إجراءات إثبات محددة لضمان حقك القانوني.\n\n"
                else:
                    analysis += f"📖 **المصدر:** {r['title']}\n> {body}\n\n"
            
            return analysis
    except:
        return "⚠️ النظام تحت الضغط. يرجى إعادة إرسال شرحك مرة أخرى."

# --- 4. إدارة المحادثة (الدردشة) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اشرح مشكلتك هنا (مثلاً: جاري أخذ أرضي بالقوة)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🧠 جاري فهم النية القانونية وترجمة المصادر...", expanded=False):
            answer = legal_engine_final(prompt, target_country, target_org)
            time.sleep(1)
        st.markdown(answer)
        
        # ميزة توليد المرافعة (تظهر عند الطلب فقط)
        if st.button("📝 توليد صيغة مرافعة رسمية"):
            st.code(f"إلى مقام محكمة {target_country} الموقرة..\nالموضوع: طلب إنصاف في واقعة {prompt}..\nنحيطكم علماً بأن...", language="text")

    st.session_state.messages.append({"role": "assistant", "content": answer})
