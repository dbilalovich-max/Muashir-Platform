import streamlit as st
import pandas as pd
import io

# 1. إعدادات الهوية البصرية والتوقيع المائي (Watermark)
st.set_page_config(page_title="منصة مؤشر - جامعة قالمة", layout="wide")

# حقن كود CSS المطور لتجميل الواجهة وإضافة التوقيع الشفاف في الخلفية
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط الخط العربي الافتراضي */
        html, body, [class*="st-"] {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }
        
        /* 1. التوقيع المائي الشفاف (Watermark) في الخلفية */
        body {
            background-color: #f8fafc; /* خلفية بيضاء ناعمة */
        }
        
        div.stApp::before {
            content: "شريكك الاستراتيجي في بناء منصات النجاح: جلابي بلال";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-25deg);
            font-size: 50px;
            font-weight: 700;
            color: rgba(0, 43, 91, 0.05); /* لون كحلي شفاف جداً جداً 5% */
            white-space: nowrap;
            pointer-events: none;
            z-index: -100; /* خلف كل العناصر */
            font-family: 'Cairo', sans-serif;
        }
        
        /* التوقيع النصي الأنيق والمثبت في الأسفل */
        .personal-sig {
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 14px;
            color: rgba(0, 43, 91, 0.6);
            background-color: rgba(255, 255, 255, 0.8);
            padding: 5px 15px;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            z-index: 1000;
        }

        /* تجميل البطاقات الإحصائية */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-top: 5px solid #00cfb2;
        }

        /* رأس الصفحة الفخم */
        .main-header {
            background: linear-gradient(90deg, #001b3d 0%, #00cfb2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        
    </style>
""", unsafe_allow_html=True)

# 2. رأس الصفحة
st.markdown('<div class="main-header"><h1>منصة "مؤشر" للتحليل الذكي للفهارس</h1><p>كلية علوم الطبيعة والحياة والملاحق - جامعة 8 ماي 1945 قالمة</p></div>', unsafe_allow_html=True)

# 3. التوقيع النصي الثابت في الأسفل
st.markdown('<div class="personal-sig"><i class="fa-solid fa-code"></i> شريك النجاح: جلابي بلال</div>', unsafe_allow_html=True)

# 4. محرك الفلترة (نفس المنطق السابق)
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
        if word.upper() in title_upper: return "مستبعد (سريري متقدم)", "غير مطابق"
    for word in keywords["الطب (أساسي)"]:
        if word.upper() in title_upper: return "قبول (أولوية)", "ملحقة الطب"
    for word in keywords["علوم الطبيعة والحياة"]:
        if word.upper() in title_upper: return "قبول", "علوم الطبيعة والحياة"
    for word in keywords["علوم الأرض والكون"]:
        if word.upper() in title_upper: return "قبول", "علوم الأرض والكون"
    for word in keywords["العلوم البيطرية"]:
        if word.upper() in title_upper: return "قبول", "العلوم البيطرية"
    return "مستبعد (خارج التخصص)", "-"

# 5. واجهة المستخدم
st.subheader("📁 رفع قائمة المورد لفلترتها")
uploaded_file = st.file_uploader("اسحب ملف الإكسل هنا لتبدأ السحر...", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    cols = [c for c in df.columns if 'Title' in str(c) or 'العنوان' in str(c) or 'title' in str(c)]
    
    if cols:
        title_col = cols[0]
        with st.spinner('جاري التصفية والتحليل...'):
            df[['القرار الذكي', 'التوجيه']] = df.apply(lambda row: pd.Series(analyze_title(row[title_col])), axis=1)
            total = len(df); acc = len(df[df['القرار الذكي'].str.contains('قبول')]); rej = total - acc
            c1, c2, c3 = st.columns(3)
            c1.metric("إجمالي الكتب", f"{total} كتاب")
            c2.metric("عناوين مطابقة للتخصص", f"{acc} كتاب")
            c3.metric("عناوين مستبعدة آلياً", f"{rej} كتاب")
            st.divider(); st.subheader("📊 الجدول التفصيلي للنتائج")
            st.dataframe(df, use_container_width=True)
            
            # زر تحميل الإكسل
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='نتائج الفلترة')
            st.download_button(label="📥 تحميل النتائج النهائية بصيغة Excel", data=buffer.getvalue(),
                               file_name="مؤشر_تقرير_الاقتناء.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("لم أتمكن من العثور على عمود باسم 'العنوان' أو 'Title'.")