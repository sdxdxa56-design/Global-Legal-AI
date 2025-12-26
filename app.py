import streamlit as st
from duckduckgo_search import DDGS
from googletrans import Translator

# إعدادات الصفحة
st.set_page_config(page_title="المحامي الذكي المطور", layout="wide")

def search_legal_advice(query, country):
    """وظيفة للبحث عن النصوص القانونية في حال عدم وجود مطابقة مباشرة"""
    try:
        with DDGS() as ddgs:
            search_query = f"قانون {query} في {country} مواد نظام"
            results = list(ddgs.text(search_query, max_results=3))
            if results:
                return "\n\n".join([r['body'] for r in results])
    except Exception as e:
        return None
    return None

# واجهة المستخدم
st.title("⚖️ المحامي الذكي (الإصدار المستقر)")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📍 الإعدادات")
    target_country = st.selectbox("اختر الدولة:", ["اليمن", "السعودية", "مصر", "الإمارات"])
    legal_reference = st.selectbox("المرجعية:", ["المحاكم الوطنية المحلية", "المحكمة الدولية (ICC)"])

with col2:
    st.subheader("💬 استشارة قانونية")
    user_input = st.text_input("اشرح قضيتك هنا (مثلاً: أريد حضانة ابني):")

    if user_input:
        with st.spinner('جاري تحليل النص والبحث في القواعد القانونية...'):
            # محاكاة البحث الذكي
            advice = search_legal_advice(user_input, target_country)
            
            if advice:
                st.success(f"✅ تم العثور على معلومات قانونية ذات صلة بـ ({target_country}):")
                st.markdown(f"**التحليل الاسترشادي:**\n\n{advice}")
                
                # أزرار إضافية كما في تصميمك
                st.divider()
                cols = st.columns(3)
                cols[0].button("📄 صياغة مرافعة")
                cols[1].button("📋 نسخ التقرير")
                cols[2].button("💾 حفظ PDF")
            else:
                st.error("⚠️ تعذر العثور على نص مباشر. يرجى تبسيط شرح المشكلة أو التأكد من اتصال الإنترنت.")

# تذييل الصفحة (Footer)
st.markdown("---")
st.caption("نظام المحامي الذكي 2024 - متوافق مع جميع الأنظمة")
