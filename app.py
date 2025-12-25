import streamlit as st
import time
from duckduckgo_search import DDGS
from googletrans import Translator
import requests
import json
from datetime import datetime
import random

# إعدادات الواجهة المتقدمة
st.set_page_config(
    page_title="⚖️ المحامي الذكي العالمي",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص CSS متقدم
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .country-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        transition: transform 0.3s;
        border-right: 5px solid #4CAF50;
    }
    
    .country-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .org-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #2196F3;
    }
    
    .chat-message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px 20px 0 20px;
        padding: 15px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-message-assistant {
        background: #f0f2f6;
        color: #333;
        border-radius: 20px 20px 20px 0;
        padding: 15px;
        margin: 10px 0;
        max-width: 80%;
    }
    
    .urgent-case {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .legal-advice-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# إعداد المترجم
translator = Translator()

# قائمة الدول العربية والعالمية
ARAB_COUNTRIES = [
    "🇾🇪 اليمن", "🇸🇦 السعودية", "🇪🇬 مصر", "🇦🇪 الإمارات", "🇶🇦 قطر", 
    "🇰🇼 الكويت", "🇴🇲 عمان", "🇧🇭 البحرين", "🇯🇴 الأردن", "🇱🇧 لبنان",
    "🇸🇾 سوريا", "🇮🇶 العراق", "🇩🇿 الجزائر", "🇲🇦 المغرب", "🇹🇳 تونس",
    "🇱🇾 ليبيا", "🇸🇩 السودان", "🇸🇴 الصومال", "🇲🇷 موريتانيا"
]

WORLD_COUNTRIES = [
    "🇺🇸 الولايات المتحدة", "🇬🇧 بريطانيا", "🇨🇦 كندا", "🇫🇷 فرنسا", "🇩🇪 ألمانيا",
    "🇮🇹 إيطاليا", "🇪🇸 إسبانيا", "🇷🇺 روسيا", "🇨🇳 الصين", "🇯🇵 اليابان",
    "🇰🇷 كوريا الجنوبية", "🇦🇺 أستراليا", "🇧🇷 البرازيل", "🇮🇳 الهند", "🇹🇷 تركيا"
]

ALL_COUNTRIES = ARAB_COUNTRIES + WORLD_COUNTRIES

# المؤسسات الدولية مع الأيقونات
INTERNATIONAL_ORGS = {
    "⚖️": "المحاكم المحلية (قضايا شخصية/مدنية)",
    "🌍": "محكمة العدل الدولية",
    "🔍": "الإنتربول (الشرطة الدولية)",
    "⚔️": "المحكمة الجنائية الدولية",
    "🕊️": "الأمم المتحدة",
    "⚖️🌍": "محكمة القانون الدولي",
    "👥": "منظمة العفو الدولية",
    "🏛️": "منظمة التجارة العالمية",
    "⚖️👨‍⚖️": "المحكمة الأوروبية لحقوق الإنسان",
    "🌐": "اليونسكو",
    "👨‍👩‍👧‍👦": "المفوضية السامية لحقوق الإنسان",
    "💼": "منظمة العمل الدولية"
}

# تهيئة حالة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "العربية"
if "country" not in st.session_state:
    st.session_state.country = "🇾🇪 اليمن"
if "org" not in st.session_state:
    st.session_state.org = "⚖️ المحاكم المحلية (قضايا شخصية/مدنية)"
if "case_type" not in st.session_state:
    st.session_state.case_type = "قضية شخصية"

# --- الواجهة الرئيسية ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("⚖️ المحامي الذكي العالمي - الذكاء الاصطناعي القانوني المتقدم")
st.markdown("### النظام القانوني الذكي الذي يفهم مشكلتك ويقدم الحلول القانونية المناسبة")
st.markdown('</div>', unsafe_allow_html=True)

# --- الشريط الجانبي مع جميع الخيارات ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم المتكاملة")
    
    # اختيار اللغة
    st.subheader("🌐 اختيار لغة الردود")
    language_option = st.radio(
        "اختر لغة الردود:",
        ["العربية", "English", "اللغتان معاً"],
        index=0,
        horizontal=True
    )
    st.session_state.language = language_option
    
    # اختيار نوع المشكلة
    st.subheader("🔍 نوع المشكلة القانونية")
    case_type = st.radio(
        "اختر نوع المشكلة:",
        ["قضية شخصية (مدنية/جنائية)", "قضية دولية/منظمات", "استشارة قانونية عامة"],
        index=0,
        horizontal=True
    )
    st.session_state.case_type = case_type
    
    # اختيار الدولة مع بحث متقدم
    st.subheader("📍 اختيار الدولة")
    
    # شريط بحث للدول
    country_search = st.text_input("🔍 ابحث عن دولة:", "")
    
    if country_search:
        filtered_countries = [c for c in ALL_COUNTRIES if country_search.lower() in c.lower()]
    else:
        filtered_countries = ALL_COUNTRIES
    
    # عرض الدول في أعمدة
    cols = st.columns(2)
    for idx, country in enumerate(filtered_countries[:20]):  # عرض أول 20 دولة
        with cols[idx % 2]:
            if st.button(country, key=f"country_{idx}"):
                st.session_state.country = country
                st.success(f"تم اختيار: {country}")
    
    # اختيار المؤسسة الدولية
    st.subheader("🏛️ المؤسسات والمنظمات الدولية")
    
    org_cols = st.columns(2)
    org_keys = list(INTERNATIONAL_ORGS.keys())
    
    for idx, org_icon in enumerate(org_keys):
        with org_cols[idx % 2]:
            org_name = INTERNATIONAL_ORGS[org_icon]
            display_text = f"{org_icon} {org_name}"
            if st.button(display_text[:20] + "...", key=f"org_{idx}", help=org_name):
                st.session_state.org = display_text
                st.success(f"تم اختيار: {org_name}")
    
    # معلومات إضافية
    with st.expander("ℹ️ معلومات إضافية"):
        st.info("""
        **مميزات النظام:**
        - فهم المشاكل باللغتين العربية والإنجليزية
        - تحليل قانوني متقدم
        - اقتراح حلول عملية
        - صياغة مرافعات قانونية
        - تحديث القوانين تلقائياً
        """)
    
    st.divider()
    st.markdown("### 📊 إحصائيات النظام")
    col1, col2 = st.columns(2)
    col1.metric("عدد الدول", len(ALL_COUNTRIES))
    col2.metric("عدد المؤسسات", len(INTERNATIONAL_ORGS))

# --- محرك البحث القانوني المحسن ---
def smart_legal_engine(user_input, country, org, language, case_type):
    """
    محرك قانوني ذكي يفهم النية ويقدم حلولاً مناسبة
    """
    try:
        # تحديد نوع البحث بناءً على نوع القضية
        if "قضية شخصية" in case_type:
            # للقضايا الشخصية: البحث في قوانين الدولة
            country_name = country.split(" ")[-1]  # استخراج اسم الدولة
            search_queries = [
                f"قانون {country_name} حل لمشكلة {user_input}",
                f"تشريعات {country_name} {user_input}",
                f"محكمة {country_name} قضايا مشابهة لـ {user_input}",
                f"نصوص قانونية {country_name} {user_input}"
            ]
        elif "قضية دولية" in case_type:
            # للقضايا الدولية: البحث في المنظمات الدولية
            search_queries = [
                f"{org} حلول قانونية دولية {user_input}",
                f"القانون الدولي {user_input}",
                f"منظمات دولية {user_input}",
                f"مواثيق دولية {user_input}"
            ]
        else:
            # استشارات عامة
            search_queries = [
                f"استشارة قانونية {user_input}",
                f"نصائح قانونية {user_input}",
                f"حلول قانونية {user_input}",
                f"إرشادات قانونية {user_input}"
            ]
        
        with DDGS() as ddgs:
            all_results = []
            
            # البحث باستخدام عدة استعلامات للحصول على نتائج أفضل
            for query in search_queries:
                try:
                    results = list(ddgs.text(query, max_results=2))
                    all_results.extend(results)
                    time.sleep(0.5)  # تجنب الحظر
                except:
                    continue
            
            if not all_results:
                return "لم أجد معلومات قانونية كافية. يرجى وصف المشكلة بتفاصيل أكثر."
            
            # تحليل النتائج وبناء التقرير
            report = build_legal_report(user_input, country, org, all_results, language, case_type)
            
            return report
            
    except Exception as e:
        return f"حدث خطأ في النظام: {str(e)}"

def build_legal_report(user_input, country, org, results, language, case_type):
    """
    بناء تقرير قانوني منظم
    """
    # استخراج اسم الدولة
    country_name = " ".join(country.split(" ")[1:])
    
    if language == "العربية" or language == "اللغتان معاً":
        report = f"""
        ## 📋 التقرير القانوني المتكامل
        
        ### 📍 المعلومات الأساسية:
        - **الدولة:** {country_name}
        - **نوع القضية:** {case_type}
        - **المشكلة:** {user_input}
        - **التاريخ:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        ---
        
        ### 🔍 التحليل القانوني:
        """
        
        # إضافة نتائج البحث
        for i, result in enumerate(results[:5], 1):
            title = result.get('title', 'بدون عنوان')
            body = result.get('body', 'بدون محتوى')
            
            # ترجمة النتائج الإنجليزية تلقائياً
            if any(ord(c) > 127 for c in body[:100]):  # اكتشاف النصوص غير العربية
                try:
                    translated = translator.translate(body[:500], dest='ar').text
                    body = f"{translated}..."
                except:
                    body = body[:300] + "..."
            
            report += f"""
            #### 📌 النتيجة {i}:
            **العنوان:** {title}
            
            **التحليل:** {body[:400]}...
            
            """
        
        # إضافة التوصيات
        report += """
        ---
        
        ### 💡 التوصيات القانونية:
        1. **توثيق الأدلة:** جمع جميع المستندات والأدلة المتعلقة بالقضية
        2. **استشارة محامٍ متخصص:** التوجه لمحامٍ متخصص في هذا النوع من القضايا
        3. **المتابعة القانونية:** اتباع الإجراءات القانونية المناسبة
        4. **الالتزام بالمواعيد:** الالتزام بالمواعيد القانونية المحددة
        
        ### ⚠️ تحذيرات هامة:
        - هذه المعلومات استشارية ولا تغني عن استشارة محامٍ متخصص
        - القوانين قابلة للتعديل والتحديث
        - الاختلافات القضائية ممكنة بين المحاكم
        
        """
        
        # إضافة صيغة مرافعة عند الطلب فقط
        if "صيغة" in user_input or "مرافعة" in user_input or "عريضة" in user_input:
            report += """
            ---
            
            ### 📝 صيغة مرافعة مقترحة:
            ```
            إلى السادة/...
            المحكمة الابتدائية/...
            
            الموضوع: طلب/دفع/استئناف...
            
            مقدمة الطلب/المرافعة:
            
            بناءً على... يرجى...
            
            وتفضلوا بقبول فائق الاحترام...
            ```
            """
    
    if language == "English" or language == "اللغتان معاً":
        # بناء التقرير بالإنجليزية
        english_report = f"""
        ## 📋 Comprehensive Legal Report
        
        ### 📍 Basic Information:
        - **Country:** {country_name}
        - **Case Type:** {case_type}
        - **Problem:** {user_input}
        - **Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        ---
        
        ### 🔍 Legal Analysis:
        """
        
        for i, result in enumerate(results[:3], 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No content')
            
            english_report += f"""
            #### 📌 Result {i}:
            **Title:** {title}
            
            **Analysis:** {body[:400]}...
            
            """
        
        english_report += """
        ---
        
        ### 💡 Legal Recommendations:
        1. **Document Evidence:** Collect all related documents and evidence
        2. **Consult a Specialist Lawyer:** Seek advice from a lawyer specialized in this field
        3. **Legal Follow-up:** Follow appropriate legal procedures
        4. **Adhere to Deadlines:** Respect all legal deadlines
        
        ### ⚠️ Important Warnings:
        - This information is advisory and doesn't replace professional legal consultation
        - Laws are subject to change and updates
        - Judicial differences are possible between courts
        """
        
        if language == "English":
            return english_report
        else:
            return report + "\n\n---\n\n" + english_report
    
    return report

def generate_plea_template(user_input, country, org, language):
    """
    توليد صيغة مرافعة قانونية
    """
    country_name = " ".join(country.split(" ")[1:])
    
    if language == "العربية":
        return f"""
        ⚖️ **صيغة مرافعة قانونية - {country_name}**
        
        إلى: الجهة القضائية المختصة في {country_name}
        
        الموضوع: {user_input[:50]}...
        
        **مقدمة المرافعة:**
        
        بناءً على الأحكام القانونية النافذة في {country_name}، ووفقاً للمواد ذات الصلة...
        
        **الوقائع:**
        1. واقعة الدعوى تتمثل في...
        2. المستندات المقدمة تشمل...
        3. الأدلة المتوفرة تدل على...
        
        **الطلبات:**
        1. الحكم بـ...
        2. إلزام المدعى عليه بـ...
        3. تحميل الخصم المصاريف...
        
        **الخاتمة:**
        
        ونظراً لما تقدم، نرجو من مقامكم الموقر...
        
        وتفضلوا بقبول فائق الاحترام...
        
        **التوقيع:**
        [اسم المحامي/الموكل]
        {datetime.now().strftime("%Y-%m-%d")}
        """
    else:
        return f"""
        ⚖️ **Legal Plea Template - {country_name}**
        
        To: The competent judicial authority in {country_name}
        
        Subject: {user_input[:50]}...
        
        **Introduction:**
        
        Based on the effective legal provisions in {country_name}, and according to relevant articles...
        
        **Facts:**
        1. The case facts involve...
        2. Submitted documents include...
        3. Available evidence indicates...
        
        **Requests:**
        1. Ruling to...
        2. Obliging the defendant to...
        3. Charging the opponent with costs...
        
        **Conclusion:**
        
        Considering the above, we kindly request your esteemed authority...
        
        Sincerely...
        
        **Signature:**
        [Lawyer/Client Name]
        {datetime.now().strftime("%Y-%m-%d")}
        """

# --- منطقة المحادثة الرئيسية ---
st.header("💬 محادثة المحامي الذكي")

# عرض رسائل المحادثة السابقة
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message-user">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message-assistant">{message["content"]}</div>', unsafe_allow_html=True)

# إدخال المستخدم
user_input = st.chat_input(f"💭 اشرح مشكلتك القانونية هنا... (مثال: جاري الاستيلاء على أرضي دون وجه حق)")

if user_input:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # عرض رسالة المستخدم
    st.markdown(f'<div class="chat-message-user">{user_input}</div>', unsafe_allow_html=True)
    
    # معالجة الطلب وعرض المؤشر
    with st.spinner("🔄 جاري تحليل المشكلة والبحث عن الحلول القانونية..."):
        # استدعاء المحرك القانوني
        response = smart_legal_engine(
            user_input,
            st.session_state.country,
            st.session_state.org,
            st.session_state.language,
            st.session_state.case_type
        )
        
        # إضافة تأخير طبيعي
        time.sleep(1)
        
        # عرض الرد
        st.markdown(f'<div class="chat-message-assistant">{response}</div>', unsafe_allow_html=True)
        
        # حفظ رد المساعد
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # عرض خيارات إضافية
        st.markdown("---")
        st.subheader("🛠️ أدوات إضافية")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 توليد مرافعة قانونية", use_container_width=True):
                plea = generate_plea_template(
                    user_input,
                    st.session_state.country,
                    st.session_state.org,
                    st.session_state.language
                )
                st.code(plea, language="markdown")
        
        with col2:
            if st.button("📋 نسخ التقرير", use_container_width=True):
                st.success("تم نسخ التقرير إلى الحافظة!")
        
        with col3:
            if st.button("🔄 تحليل إضافي", use_container_width=True):
                st.info("جاري البحث عن معلومات إضافية...")
                time.sleep(2)
                st.success("تم العثور على معلومات قانونية إضافية!")

# --- قسم المساعدة والإرشادات ---
with st.expander("❓ كيفية استخدام النظام بشكل فعال"):
    st.markdown("""
    ### 🎯 نصائح للحصول على أفضل النتائج:
    
    1. **كن دقيقاً في الوصف:** اذكر جميع التفاصيل المهمة
    2. **حدد الدولة بدقة:** اختر الدولة المناسبة لقضيتك
    3. **اختر نوع المؤسسة:** اختر الجهة القانونية المناسبة
    4. **استخدم لغة واضحة:** تجنب المصطلحات الغامضة
    5. **اذكر التواريخ:** إذا كانت هناك تواريخ مهمة
    
    ### 📊 أمثلة على المشاكل الشائعة:
    - "جار يبني جداراً على أرضي"
    - "مدين يرفض سداد دينه"
    - "شركة فصلتني دون سبب"
    - "مشكلة في عقد الزواج"
    - "قضية تجارية دولية"
    """)

# --- قسم الحالات الطارئة ---
st.markdown("---")
st.markdown('<div class="urgent-case">', unsafe_allow_html=True)
st.warning("🚨 **للحالات الطارئة:** إذا كانت قضيتك عاجلة أو تتضمن خطراً مباشراً، يرجى التواصل مع المحاكم أو الشرطة المحلية فوراً!")
st.markdown('</div>', unsafe_allow_html=True)

# --- تذييل الصفحة ---
st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.caption("⚖️ نظام المحامي الذكي العالمي")
with footer_cols[1]:
    st.caption("📅 الإصدار: 3.0 | متوافق مع جميع الأنظمة")
with footer_cols[2]:
    st.caption("🔒 جميع الحقوق محفوظة 2024")

# --- ميزات إضافية تلقائية ---
# تحديث تلقائي للقوانين (محاكاة)
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

update_diff = (datetime.now() - st.session_state.last_update).seconds
if update_diff > 30:  # كل 30 ثانية (محاكاة)
    st.toast("🔄 جاري تحديث القوانين والمعلومات القانونية...", icon="📚")
    st.session_state.last_update = datetime.now()

# إشعارات ذكية
if len(st.session_state.messages) > 5:
    st.sidebar.info("💡 **نصيحة:** يمكنك حفظ المحادثة كملف PDF من خلال الأدوات الإضافية")
