import streamlit as st
import pandas as pd
import io

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="منصة مؤشر - جامعة قالمة", layout="wide", page_icon="📚")

# حقن كود CSS (تم إصلاح تشوهات RTL وإضافة تنسيقات الرموز)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* تطبيق الخط والاتجاه بشكل آمن لتفادي تشوه الأيقونات */
        .block-container {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }
        
        /* حماية القائمة العلوية وزر الرفع من تشوهات RTL */
        header[data-testid="stHeader"] { direction: ltr !important; }
        .stFileUploader section > div { direction: ltr !important; }
        .stFileUploader { direction: rtl; }
        
        /* 1. التوقيع المائي الشفاف (Watermark) */
        body { background-color: #f8fafc; }
        div.stApp::before {
            content: "شريكك الاستراتيجي في بناء منصات النجاح: جلابي بلال";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-25deg);
            font-size: 50px;
            font-weight: 700;
            color: rgba(0, 43, 91, 0.04); 
            white-space: nowrap;
            pointer-events: none;
            z-index: -100;
            font-family: 'Cairo', sans-serif;
        }
        
        /* التوقيع النصي الأنيق والمثبت في الأسفل */
        .personal-sig {
            position: fixed; bottom: 10px; left: 10px; font-size: 14px;
            color: rgba(0, 43, 91, 0.6); background-color: rgba(255, 255, 255, 0.8);
            padding: 5px 15px; border-radius: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 1000;
        }

        /* رأس الصفحة الفخم */
        .main-header {
            background: linear-gradient(90deg, #001b3d 0%, #00cfb2 100%);
            color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center;
            box-shadow: 0 10px 20px rgba(0,207,178,0.2);
        }
        
        /* تصميم بطاقات الكليات (الأيقونات) */
        .faculty-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
            border: 1px solid #00cfb2; border-radius: 12px; padding: 15px;
            text-align: center; font-weight: bold; color: #001b3d;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.3s ease;
            height: 100%;
        }
        .faculty-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,207,178,0.15); }
        .fac-icon { font-size: 40px; margin-bottom: 10px; display: block; }

        /* تجميل البطاقات الإحصائية */
        div[data-testid="stMetric"] {
            background-color: #ffffff; border: 1px solid #e0e0e0; padding: 20px;
            border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #00cfb2;
        }
    </style>
""", unsafe_allow_html=True)

# 2. رأس الصفحة
st.markdown('<div class="main-header"><h1>📚 منصة "مؤشر" للتحليل الذكي للفهارس</h1><p>المكتبة المركزية - جامعة 8 ماي 1945 قالمة</p></div>', unsafe_allow_html=True)

# 3. شريط الكليات والأيقونات (الجانب البصري الجديد)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='faculty-card'><span class='fac-icon'>🩺</span>الملحقة الطبية<br><small>العلوم الأساسية</small></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='faculty-card'><span class='fac-icon'>🧬</span>علوم الطبيعة والحياة<br><small>البيولوجيا والبيئة</small></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='faculty-card'><span class='fac-icon'>🌍</span>علوم الأرض والكون<br><small>الجيولوجيا والفلك</small></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='faculty-card'><span class='fac-icon'>🐾</span>العلوم البيطرية<br><small>التشريح والأمراض</small></div>", unsafe_allow_html=True)

st.write("") # مسافة فارغة
st.divider()

# 4. التوقيع النصي
st.markdown('<div class="personal-sig"><i class="fa-solid fa-code"></i> شريك النجاح: جلابي بلال</div>', unsafe_allow_html=True)

# 5. محرك الفلترة الذكي
keywords = {
    "الطب (أساسي)": ["Anatomy", "Physiology", "Pathology", "Biochemistry", "Pharmacology", "Histology"],
    "الطب (استبعاد سريري)": ["Surgery", "Pediatrics", "Obstetrics", "Internal Medicine"],
    "علوم الطبيعة والحياة": ["Biology", "Genetics", "Microbiology", "Ecology", "Biotechnology", "Cellular"],
    "علوم الأرض والكون": ["Geology", "Cosmology", "Tectonics", "Petrology", "Oceanography"],
    "العلوم البيطرية": ["Veterinary", "Animal Anatomy", "Zoonotic", "Dyce", "الطفيليات البيطرية"]
}

def analyze_title(title):
    title_upper = str(title).upper()
    for word in keywords["الطب (استبعاد سريري)"]:
        if word.upper() in title_upper: return "مستبعد 🔴 (سريري)", "غير مطابق"
    for word in keywords["الطب (أساسي)"]:
        if word.upper() in title_upper: return "قبول 🟢", "الملحقة الطبية 🩺"
    for word in keywords["علوم الطبيعة والحياة"]:
        if word.upper() in title_upper: return "قبول 🟢", "علوم الطبيعة 🧬"
    for word in keywords["علوم الأرض والكون"]:
        if word.upper() in title_upper: return "قبول 🟢", "علوم الأرض 🌍"
    for word in keywords["العلوم البيطرية"]:
        if word.upper() in title_upper: return "قبول 🟢", "البيطرة 🐾"
    return "مستبعد ⚪ (خارج النطاق)", "-"

# 6. واجهة الرفع والنتائج
st.subheader("📁 مساحة العمل: رفع قائمة المورد")
uploaded_file = st.file_uploader("قم بإسقاط ملف الإكسل (Excel) هنا لتبدأ عملية الفلترة الذكية...", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    cols = [c for c in df.columns if 'Title' in str(c) or 'العنوان' in str(c) or 'title' in str(c)]
    
    if cols:
        title_col = cols[0]
        with st.spinner('يتم الآن فحص العناوين وتوجيهها...'):
            df[['القرار الذكي', 'التوجيه (القسم)']] = df.apply(lambda row: pd.Series(analyze_title(row[title_col])), axis=1)
            total = len(df); acc = len(df[df['القرار الذكي'].str.contains('قبول')]); rej = total - acc
            
            c1, c2, c3 = st.columns(3)
            c1.metric("📚 إجمالي الكتب الواردة", f"{total} كتاب")
            c2.metric("✅ عناوين مطابقة للمناهج", f"{acc} كتاب")
            c3.metric("❌ عناوين مستبعدة آلياً", f"{rej} كتاب")
            
            st.divider()
            st.subheader("📊 تقرير الفلترة التفصيلي")
            st.dataframe(df, use_container_width=True)
            
            # زر التحميل
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='النتائج_النهائية')
            st.download_button(label="📥 تصدير النتائج بصيغة Excel", data=buffer.getvalue(),
                               file_name="مؤشر_تقرير_الاقتناء.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("تنبيه: لم يتم العثور على عمود باسم 'العنوان' أو 'Title'. يرجى التأكد من رأس الجدول في الملف.")