import streamlit as st
import time
import json
import re
from duckduckgo_search import DDGS
from googletrans import Translator
import requests
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
import pickle
from collections import defaultdict

# إعدادات الواجهة
st.set_page_config(page_title="⚖️ المحامي الذكي - فهم عميق للهجات", layout="wide")

# تخصيص CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Tajawal:wght@300;500;700&display=swap');
    
    * {
        font-family: 'Cairo', 'Tajawal', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .urgent-alert {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        animation: pulse 1.5s infinite;
        margin: 20px 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .solution-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-right: 6px solid #4CAF50;
    }
    
    .dialect-badge {
        background: #FF9800;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8em;
        margin: 0 5px;
    }
    
    .step-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: white;
        border-radius: 25px 25px 5px 25px;
        padding: 18px;
        margin: 15px 0;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .chat-bubble-ai {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        color: white;
        border-radius: 25px 25px 25px 5px;
        padding: 18px;
        margin: 15px 0;
        max-width: 85%;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# قاموس اللهجات والمصطلحات العامية
DIALECT_DICTIONARY = {
    # لهجات يمنية
    "مشتبه بي": ["اتهام", "شبهة", "توجيه تهمة", "اشتباه"],
    "أنا مظلوم": ["تعرضت للظلم", "تعرضت لإجحاف", "انتهكت حقوقي"],
    "حرامي": ["سارق", "ناهب", "معتدٍ على الممتلكات"],
    "غصبني": ["استولى بالقوة", "اغتصب حق", "انتزع ملكية"],
    "خانني": ["خيانة الأمانة", "إخلال بالثقة", "نقض العهد"],
    "طقاق": ["نزاع أسري", "خلاف زوجي", "شقاق"],
    "ضايقني": ["تحرش", "إيذاء نفسي", "مضايقة"],
    
    # لهجات سعودية
    "واذي": ["أذى", "إيذاء", "ضرر"],
    "غشني": ["احتيال", "تدليس", "غش"],
    "طقع": ["إفلاس", "إعسار", "عجز مالي"],
    "سرقلي": ["سرقة", "اختلاس", "أخذ بدون وجه حق"],
    
    # لهجات مصرية
    "اتشحت": ["سرقت", "نُهبت", "سُلب"],
    "اتعرضت لظلم": ["تعرضت للاضطهاد", "انتهكت حقوقي"],
    "حد غلط في حقي": ["اعتدى على حقوقي", "ألحق بي ضرراً"],
    "عاوز حقى": ["أطالب بحقي", "أنشد العدالة"],
    
    # لهجات خليجية
    "أنا مظلوم": ["مغلوب على أمري", "منتهك الحقوق"],
    "يظلموني": ["يضطهدونني", "ينتهكون حقي"],
    "خذوا حقي": ["استولوا على ملكيتي", "سلبوا حقوقي"],
}

# قاموس الجرائم والمشاكل القانونية
LEGAL_ISSUES = {
    "قتل": {
        "category": "جنائي",
        "keywords": ["قتل", "قتل عمد", "قتل خطأ", "جريمة قتل", "مقتول", "قتيل", "يقتل"],
        "steps": [
            "الإبلاغ الفوري للشرطة",
            "تقديم بلاغ رسمي",
            "طلب تشريح الجثة",
            "جمع الأدلة والشهود",
            "تعيين محامٍ جنائي متخصص",
            "المطالبة بالقصاص أو الدية"
        ],
        "articles": ["المادة 126", "المادة 127", "المادة 128"],
        "evidence": ["شهادة الشهود", "تقرير الطبيب الشرعي", "الأدلة المادية", "التسجيلات المرئية"]
    },
    "سرقة": {
        "category": "جنائي",
        "keywords": ["سرقة", "سارق", "مسروق", "نهب", "اختلاس"],
        "steps": [
            "الإبلاغ للشرطة",
            "تقديم قائمة بالمفقودات",
            "طلب كاميرات المراقبة",
            "تقديم بلاغ في النيابة",
            "المطالبة بالتعويض"
        ]
    },
    "تزوير": {
        "category": "جنائي",
        "keywords": ["تزوير", "مزور", "تزييف", "تزوير وثائق"],
        "steps": [
            "فحص الوثيقة من خبير",
            "تقديم بلاغ تزوير",
            "تقديم الدعوى الجزائية",
            "طلب تعويض عن الضرر"
        ]
    },
    "تحرش": {
        "category": "جنائي",
        "keywords": ["تحرش", "مضايقة", "تحرش جنسي", "تحرش لفظي"],
        "steps": [
            "توثيق الحادثة",
            "جمع الأدلة (رسائل، تسجيلات)",
            "الإبلاغ للشرطة",
            "تقديم شكوى رسمية",
            "طلب الحماية القانونية"
        ]
    },
    "نزاع أرض": {
        "category": "مدني",
        "keywords": ["أرض", "مزرعة", "عقار", "ملكية", "حيازة"],
        "steps": [
            "تقديم سند الملكية",
            "طلب كشف رسمي",
            "رفع دعوى استحقاق",
            "طلب منع التصرف",
            "تنفيذ الحكم القضائي"
        ]
    },
    "دين": {
        "category": "مدني",
        "keywords": ["دين", "مدين", "سلف", "قرض", "مستحق"],
        "steps": [
            "تقديم إثبات الدين (إيصال، عقد)",
            "إرسال إنذار رسمي",
            "رفع دعوى استحقاق",
            "طلب حجز أموال",
            "تنفيذ الحكم"
        ]
    },
    "طلاق": {
        "category": "أحوال شخصية",
        "keywords": ["طلاق", "خلع", "تفريق", "فراق", "شقاق"],
        "steps": [
            "محاولة الصلح",
            "رفع دعوى الطلاق",
            "تحديد المهر والمؤخر",
            "طلب النفقة والحضانة",
            "تنفيذ الأحكام"
        ]
    }
}

# قائمة الدول العربية
ARAB_COUNTRIES = [
    "🇾🇪 اليمن", "🇸🇦 السعودية", "🇪🇬 مصر", "🇦🇪 الإمارات", 
    "🇶🇦 قطر", "🇰🇼 الكويت", "🇴🇲 عمان", "🇧🇭 البحرين",
    "🇯🇴 الأردن", "🇱🇧 لبنان", "🇸🇾 سوريا", "🇮🇶 العراق",
    "🇩🇿 الجزائر", "🇲🇦 المغرب", "🇹🇳 تونس", "🇱🇾 ليبيا",
    "🇸🇩 السودان", "🇸🇴 الصومال", "🇲🇷 موريتانيا"
]

# قوانين الدول (محاكاة)
COUNTRY_LAWS = {
    "اليمن": {
        "قتل عمد": "السجن المؤبد أو الإعدام",
        "قتل خطأ": "الدية والسجن",
        "سرقة": "السجن والقطع",
        "تزوير": "السجن والغرامة"
    },
    "السعودية": {
        "قتل عمد": "القصاص أو الدية",
        "قتل خطأ": "الدية والتعزير",
        "سرقة": "قطع اليد أو السجن",
        "تزوير": "السجن والغرامة"
    },
    "مصر": {
        "قتل عمد": "السجن المؤبد أو الإعدام",
        "قتل خطأ": "السجن والغرامة",
        "سرقة": "السجن والغرامة",
        "تزوير": "السجن والغرامة"
    }
}

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "العربية"
if "country" not in st.session_state:
    st.session_state.country = "🇾🇪 اليمن"

# --- الدوال الأساسية ---
def detect_dialect(text):
    """كشف اللهجة والمصطلحات العامية"""
    detected_dialects = []
    normalized_text = text
    
    for dialect_word, formal_words in DIALECT_DICTIONARY.items():
        if dialect_word in text:
            detected_dialects.append({
                "dialect": dialect_word,
                "formal": formal_words[0],
                "all_formal": formal_words
            })
            # استبدال المصطلح العامي بالفصيح
            normalized_text = normalized_text.replace(dialect_word, formal_words[0])
    
    return normalized_text, detected_dialects

def understand_problem(user_input):
    """فهم المشكلة من الوصف الطبيعي"""
    # كشف اللهجة
    normalized_text, dialects = detect_dialect(user_input)
    
    # تحليل النص لفهم المشكلة
    problem_type = None
    details = {}
    
    # البحث عن نوع المشكلة
    for issue, data in LEGAL_ISSUES.items():
        for keyword in data["keywords"]:
            if keyword in normalized_text or keyword in user_input:
                problem_type = issue
                details = data
                break
        if problem_type:
            break
    
    # إذا لم يتم التعرف، استخدام الذكاء الاصطناعي للاستنتاج
    if not problem_type:
        problem_type = infer_problem_type(normalized_text)
    
    return {
        "original_text": user_input,
        "normalized_text": normalized_text,
        "dialects_found": dialects,
        "problem_type": problem_type,
        "problem_details": details,
        "is_urgent": check_urgency(user_input)
    }

def infer_problem_type(text):
    """استنتاج نوع المشكلة من السياق"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["قتل", "مقتول", "قتيل", "يقتل"]):
        return "قتل"
    elif any(word in text_lower for word in ["سرق", "سارق", "مسروق", "نهب"]):
        return "سرقة"
    elif any(word in text_lower for word in ["غش", "احتيال", "تدليس"]):
        return "احتيال"
    elif any(word in text_lower for word in ["تحرش", "مضايقة", "تحرش جنسي"]):
        return "تحرش"
    elif any(word in text_lower for word in ["أرض", "عقار", "ملكية", "مزرعة"]):
        return "نزاع أرض"
    elif any(word in text_lower for word in ["دين", "قرض", "سلف", "مدين"]):
        return "دين"
    elif any(word in text_lower for word in ["طلاق", "خلع", "فراق", "زواج"]):
        return "طلاق"
    else:
        return "قضية عامة"

def check_urgency(text):
    """فحص إذا كانت القضية عاجلة"""
    urgent_keywords = ["قتل", "تهديد", "خطف", "اغتصاب", "حرق", "انتحار", "حادث"]
    return any(keyword in text for keyword in urgent_keywords)

def get_country_name(country_emoji):
    """استخراج اسم الدولة من الرمز"""
    return country_emoji.split(" ", 1)[1]

def generate_solution(problem_analysis, country):
    """توليد حل قانوني تفصيلي"""
    country_name = get_country_name(country)
    problem_type = problem_analysis["problem_type"]
    
    solution = {
        "title": f"الحل القانوني لمشكلة: {problem_type}",
        "country": country_name,
        "urgency": "عاجلة" if problem_analysis["is_urgent"] else "عادية",
        "steps": [],
        "laws": [],
        "advice": []
    }
    
    # إضافة الخطوات القانونية
    if problem_analysis["problem_details"] and "steps" in problem_analysis["problem_details"]:
        solution["steps"] = problem_analysis["problem_details"]["steps"]
    else:
        # خطوات عامة
        solution["steps"] = [
            f"١. التوجه إلى أقرب مركز شرطة في {country_name} لتقديم بلاغ",
            f"٢. طلب نسخة رسمية من البلاغ",
            f"٣. التوجه للنيابة العامة لتسجيل الدعوى",
            f"٤. تعيين محامٍ متخصص في قضايا {problem_type}",
            f"٥. جمع جميع الأدلة والمستندات",
            f"٦. متابعة الدعوى بشكل منتظم"
        ]
    
    # إضافة القوانين ذات الصلة
    if country_name in COUNTRY_LAWS and problem_type in COUNTRY_LAWS[country_name]:
        solution["laws"].append(f"العقوبة في {country_name}: {COUNTRY_LAWS[country_name][problem_type]}")
    
    # نصائح إضافية
    if problem_analysis["is_urgent"]:
        solution["advice"].append("🚨 هذه قضية عاجلة، يجب التصرف فوراً")
        solution["advice"].append("📞 اتصل برقم الطوارئ المحلي على الفور")
    
    solution["advice"].append("📋 احتفظ بنسخ من جميع المستندات")
    solution["advice"].append("⏰ التزم بالمواعيد القانونية")
    solution["advice"].append("🤝 استشر أكثر من محامٍ قبل التعيين")
    
    return solution

def format_solution(solution, problem_analysis):
    """تنسيق الحل بشكل جميل"""
    country_name = solution["country"]
    
    output = f"""
    <div style='background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%); color: white; padding: 25px; border-radius: 20px; margin: 20px 0;'>
        <h2>⚖️ الحل القانوني في {country_name}</h2>
        <h3>المشكلة: {problem_analysis['problem_type']}</h3>
        <p><strong>الحالة:</strong> {'🚨 حالة عاجلة' if problem_analysis['is_urgent'] else '📄 حالة عادية'}</p>
    </div>
    
    <div class='solution-card'>
        <h3>📋 الخطوات القانونية المطلوبة:</h3>
        <ol style='padding-right: 20px;'>
    """
    
    for i, step in enumerate(solution["steps"], 1):
        output += f"<li style='margin-bottom: 10px;'>{step}</li>"
    
    output += """
        </ol>
    </div>
    """
    
    if solution["laws"]:
        output += f"""
        <div style='background: #4CAF50; color: white; padding: 20px; border-radius: 15px; margin: 20px 0;'>
            <h3>📜 القوانين ذات الصلة:</h3>
            <ul>
        """
        for law in solution["laws"]:
            output += f"<li>{law}</li>"
        output += "</ul></div>"
    
    if solution["advice"]:
        output += """
        <div style='background: #FF9800; color: white; padding: 20px; border-radius: 15px; margin: 20px 0;'>
            <h3>💡 نصائح مهمة:</h3>
            <ul>
        """
        for advice in solution["advice"]:
            output += f"<li>{advice}</li>"
        output += "</ul></div>"
    
    # إضافة قسم الطوارئ إذا كانت الحالة عاجلة
    if problem_analysis["is_urgent"]:
        output += """
        <div class='urgent-alert'>
            <h3>🚨 إجراءات الطوارئ:</h3>
            <p>١. اتصل بالشرطة فوراً: ١١١</p>
            <p>٢. توجه لأقرب مستشفى إذا كان هناك إصابات</p>
            <p>٣. لا تغير موقع الحادث</p>
            <p>٤. احصل على أرقام هواتف الشهود</p>
        </div>
        """
    
    return output

def search_legal_info(query, country):
    """الببحث عن معلومات قانونية إضافية"""
    try:
        with DDGS() as ddgs:
            country_name = get_country_name(country)
            search_query = f"قانون {country_name} {query}"
            results = list(ddgs.text(search_query, max_results=3))
            
            if results:
                info = "### 🔍 معلومات قانونية إضافية:\n\n"
                for i, result in enumerate(results, 1):
                    title = result.get('title', '')
                    body = result.get('body', '')[:200]
                    info += f"**{i}. {title}**\n"
                    info += f"{body}...\n\n"
                return info
            return ""
    except:
        return ""

# --- الواجهة الرئيسية ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("⚖️ المحامي الذكي - يفهم اللهجات والمصطلحات العامية")
st.markdown("### 💬 اشرح مشكلتك بأي لهجة وسأقدم لك الحل القانوني المناسب")
st.markdown('</div>', unsafe_allow_html=True)

# --- الشريط الجانبي ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # اختيار الدولة
    st.subheader("📍 اختر دولتك")
    selected_country = st.selectbox(
        "الدولة:",
        ARAB_COUNTRIES,
        index=0
    )
    st.session_state.country = selected_country
    
    # اختيار اللغة
    st.subheader("🌐 لغة الرد")
    language_option = st.radio(
        "اللغة:",
        ["العربية فقط", "العربية والإنجليزية"],
        horizontal=True
    )
    
    # معلومات عن النظام
    st.divider()
    st.subheader("ℹ️ عن النظام")
    st.info("""
    النظام يفهم:
    - جميع اللهجات العربية
    - المصطلحات العامية
    - الوصف الطبيعي للمشاكل
    - لا حاجة لصياغة قانونية
    """)
    
    st.divider()
    st.success("✅ النظام جاهز لاستقبال مشكلتك")

# --- منطقة المحادثة الرئيسية ---
st.header("💬 اشرح مشكلتك هنا")

# مثال على المشاكل
with st.expander("📋 أمثلة على كيفية الشرح:"):
    examples = st.columns(3)
    
    with examples[0]:
        st.markdown("""
        **مشاكل جنائية:**
        - أنا مشتبه بي بقتل صديقي
        - جاري سرق مني أموال
        - واحد غشني في تجارة
        - حد تحرش بابنتي
        """)
    
    with examples[1]:
        st.markdown("""
        **مشاكل مدنية:**
        - أخي أخذ أرضي
        - واحد مديني فلوس ومش رادها
        - الشركة غلطت في حقي
        - العقد ظالم
        """)
    
    with examples[2]:
        st.markdown("""
        **مشاكل أسرية:**
        - أريد أطلق من زوجتي
        - أبوي مانعني من الزواج
        - أمي تظلمني في الميراث
        - العائلة متداخلة في حياتي
        """)

# إدخال المستخدم
user_input = st.text_area(
    "💭 اشرح مشكلتك بشكل طبيعي:",
    placeholder="مثال: أنا مشتبه بي بقتل صديقي وأنا بريء...",
    height=120
)

# زر التحليل
if st.button("🔍 تحليل المشكلة وإيجاد الحل", type="primary", use_container_width=True):
    if user_input:
        # عرض رسالة المستخدم
        st.markdown(f'<div class="chat-bubble-user">{user_input}</div>', unsafe_allow_html=True)
        
        # تحليل المشكلة مع مؤشر التحميل
        with st.spinner("🤔 جاري فهم مشكلتك وتحليلها..."):
            time.sleep(1.5)
            
            # فهم المشكلة
            problem_analysis = understand_problem(user_input)
            
            # عرض تحليل المشكلة
            st.markdown(f"""
            <div style='background: #f0f2f6; padding: 20px; border-radius: 15px; margin: 20px 0;'>
                <h3>🔍 تحليل المشكلة:</h3>
                <p><strong>المشكلة المحددة:</strong> {problem_analysis['problem_type']}</p>
                <p><strong>التصنيف:</strong> {problem_analysis['problem_details'].get('category', 'قضية قانونية')}</p>
                <p><strong>الحالة:</strong> {'🚨 حالة عاجلة' if problem_analysis['is_urgent'] else '📄 حالة عادية'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # عرض اللهجات المكتشفة
            if problem_analysis["dialects_found"]:
                st.markdown("### 🗣️ فهمت اللهجة:")
                cols = st.columns(3)
                for i, dialect in enumerate(problem_analysis["dialects_found"][:3]):
                    with cols[i]:
                        st.markdown(f"""
                        <div style='background: #FF9800; color: white; padding: 10px; border-radius: 10px; text-align: center;'>
                            <strong>{dialect['dialect']}</strong><br>
                            → {dialect['formal']}
                        </div>
                        """, unsafe_allow_html=True)
        
        # توليد الحل
        with st.spinner("⚖️ جاري إعداد الحل القانوني المناسب..."):
            time.sleep(2)
            
            # توليد الحل
            solution = generate_solution(problem_analysis, st.session_state.country)
            
            # عرض الحل
            st.markdown(format_solution(solution, problem_analysis), unsafe_allow_html=True)
            
            # بحث عن معلومات إضافية
            additional_info = search_legal_info(problem_analysis["problem_type"], st.session_state.country)
            if additional_info:
                st.markdown(additional_info)
            
            # زر لحفظ النصائح
            if st.button("💾 حفظ النصائح كملف نصي"):
                advice_text = f"""
                النصائح القانونية:
                المشكلة: {problem_analysis['problem_type']}
                الدولة: {solution['country']}
                
                الخطوات:
                {chr(10).join(solution['steps'])}
                
                القوانين:
                {chr(10).join(solution['laws'])}
                
                النصائح:
                {chr(10).join(solution['advice'])}
                """
                st.download_button(
                    label="📥 تنزيل النصائح",
                    data=advice_text,
                    file_name=f"نصائح_قانونية_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
    else:
        st.warning("⚠️ الرجاء إدخال وصف لمشكلتك أولاً")

# --- قسم الطوارئ السريع ---
st.markdown("---")
st.markdown('<div class="urgent-alert">', unsafe_allow_html=True)
st.markdown("### 🚨 للقضايا العاجلة فوراً:")
emergency_cols = st.columns(4)

with emergency_cols[0]:
    if st.button("🚓 اتصال بالشرطة", use_container_width=True):
        st.info("رقم الطوارئ: ١١١ أو ٩١١")

with emergency_cols[1]:
    if st.button("🏥 إسعاف", use_container_width=True):
        st.info("رقم الإسعاف: ٩٩٩")

with emergency_cols[2]:
    if st.button("🚒 إطفاء", use_container_width=True):
        st.info("رقم الإطفاء: ٩٩٨")

with emergency_cols[3]:
    if st.button("⚖️ محامي طوارئ", use_container_width=True):
        st.info("جاري البحث عن أقرب محامٍ متاح...")

st.markdown('</div>', unsafe_allow_html=True)

# --- قسم الأسئلة الشائعة ---
with st.expander("❓ كيف يعمل النظام؟"):
    st.markdown("""
    ### 🤖 آلية العمل:
    
    1. **الفهم الذكي**: النظام يفهم اللهجات والمصطلحات العامية
    2. **تحليل السياق**: يحدد نوع المشكلة القانونية تلقائياً
    3. **التخصيص**: يطبق قوانين الدولة المختارة
    4. **تقديم الحل**: يقدم خطوات عملية مفصلة
    
    ### 💡 نصائح للحصول على أفضل نتيجة:
    - اشرح المشكلة كما تحكيها لأحد الأصدقاء
    - لا تحتاج لاستخدام مصطلحات قانونية
    - اذكر جميع التفاصيل المهمة
    - حدد دولتك بدقة
    """)

# --- قسم المحاكاة الذكية ---
st.markdown("---")
st.subheader("🎯 جرب بنفسك - أمثلة جاهزة")

example_cols = st.columns(4)

with example_cols[0]:
    if st.button("قتل/اتهام", use_container_width=True):
        st.session_state.demo_text = "أنا مشتبه بي بقتل صديقي وأنا بريء، الشرطة تبحث عني"

with example_cols[1]:
    if st.button("سرقة أرض", use_container_width=True):
        st.session_state.demo_text = "جاري غصب أرضي وبني فيها بدون إذني"

with example_cols[2]:
    if st.button("تحرش", use_container_width=True):
        st.session_state.demo_text = "مديري في الشغل يتحرش فيني ويضايقني"

with example_cols[3]:
    if st.button("دين", use_container_width=True):
        st.session_state.demo_text = "واحد مديني فلوس ومن سنة ومش رادها لي"

if 'demo_text' in st.session_state:
    user_input = st.session_state.demo_text
    st.text_area("💭 مثال جاهز:", value=user_input, height=100, disabled=True)
    if st.button("🔍 تحليل هذا المثال", type="secondary"):
        # إعادة تحميل الصفحة بالمثال
        st.rerun()

# --- تذييل الصفحة ---
st.markdown("---")
footer = st.columns(3)
with footer[0]:
    st.caption("⚖️ نظام المحامي الذكي المتقدم")
with footer[1]:
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with footer[2]:
    st.caption("💡 يفهم جميع اللهجات العربية")
