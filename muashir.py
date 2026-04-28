import streamlit as st
import pandas as pd
import io

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="منصة مؤشر | Muashir Platform", layout="wide", page_icon="📚")

# 2. القاموس اللغوي الشامل (الآن يحتوي على كل المفاتيح لتفادي خطأ KeyError)
translations = {
    "AR": {
        "title": "📚 منصة \"مؤشر\" للتحليل الذكي لفهارس العناوين",
        "subtitle": "مكتبة علوم الطبيعة والحياة وعلوم الأرض والكون - جامعة 8 ماي 1945 قالمة",
        "upload_title": "📁 مساحة العمل: رفع قائمة المورد",
        "select_col": "⚠️ لم أتعرف على عمود العناوين تلقائياً، يرجى اختياره من القائمة:",
        "processing": "جاري فحص وتوجيه العناوين...",
        "total_books": "📚 إجمالي الكتب", "accepted": "✅ مطابقة", "rejected": "❌ مستبعدة",
        "download_btn": "📥 تصدير النتائج (Excel)",
        "sig": "شريك النجاح: جلابي بلال", "dir": "rtl",
        "vet_title": "العلوم البيطرية 🐾", "med_title": "الملحقة الطبية 🩺",
        "bio_title": "علوم الطبيعة 🧬", "earth_title": "علوم الأرض 🌍",
        "dec_acc_vet": "قبول 🟢 (بيطرة)", "dec_rej_clin": "مستبعد 🔴 (سريري)",
        "dec_acc_med": "قبول 🟢 (طب)", "dec_acc_bio": "قبول 🟢 (بيولوجيا)",
        "dec_acc_earth": "قبول 🟢 (أرض)", "dec_out": "مستبعد ⚪ (خارج النطاق)"
    },
    "EN": {
        "title": "📚 'Muashir' Smart Catalog Analysis",
        "subtitle": "Faculty of Natural and Life Sciences, Earth and the Universe Library - University of 8 Mai 1945 Guelma",
        "upload_title": "📁 Workspace: Upload Supplier List",
        "select_col": "⚠️ Could not auto-detect the Title column. Please select it:",
        "processing": "Analyzing and routing...",
        "total_books": "📚 Total Books", "accepted": "✅ Accepted", "rejected": "❌ Rejected",
        "download_btn": "📥 Export to Excel",
        "sig": "Success Partner: DJELLABI Bilal", "dir": "ltr",
        "vet_title": "Veterinary 🐾", "med_title": "Medicine 🩺",
        "bio_title": "Biology 🧬", "earth_title": "Earth Sci 🌍",
        "dec_acc_vet": "Accepted 🟢 (Vet)", "dec_rej_clin": "Rejected 🔴 (Clinical)",
        "dec_acc_med": "Accepted 🟢 (Med)", "dec_acc_bio": "Accepted 🟢 (Bio)",
        "dec_acc_earth": "Accepted 🟢 (Earth)", "dec_out": "Out of Scope ⚪"
    },
    "ZH": {
        "title": "📚 “Muashir” 智能书目分析平台",
        "subtitle": "Faculty of Natural and Life Sciences, Earth and the Universe Library - University of 8 Mai 1945 Guelma",
        "upload_title": "📁 工作区：上传清单",
        "select_col": "⚠️ 无法自动识别标题列，请手动选择：",
        "processing": "分析中...",
        "total_books": "📚 总数", "accepted": "✅ 已接受", "rejected": "❌ 已拒绝",
        "download_btn": "📥 导出 Excel",
        "sig": "合作伙伴：DJELLABI Bilal", "dir": "ltr",
        "vet_title": "兽医学 🐾", "med_title": "医学 🩺",
        "bio_title": "生物学 🧬", "earth_title": "地球科学 🌍",
        "dec_acc_vet": "接受 🟢 (兽医)", "dec_rej_clin": "拒绝 🔴 (临床)",
        "dec_acc_med": "接受 🟢 (医学)", "dec_acc_bio": "接受 🟢 (生物)",
        "dec_acc_earth": "接受 🟢 (地球)", "dec_out": "超出范围 ⚪"
    }
}

# 3. اختيار اللغة
st.sidebar.title("🌐 Language")
lang_choice = st.sidebar.radio("", ["العربية", "English", "中文"])
lang = "AR" if lang_choice == "العربية" else ("EN" if lang_choice == "English" else "ZH")
t = translations[lang]

# 4. محرك الفلترة (بالأولويات المصححة والكلمات الموسعة)
keywords = {
    "vet_inc": ["Veterinary", "Animal", "Animals", "Zoonotic", "Dyce", "الطفيليات البيطرية", "Domestic", "Equine", "Poultry", "Livestock"],
    "med_ex": ["Surgery", "Pediatrics", "Obstetrics", "Internal Medicine", "Clinical"],
    "med_inc": ["Anatomy", "Physiology", "Pathology", "Biochemistry", "Pharmacology", "Histology"],
    "bio_inc": ["Biology", "Genetics", "Microbiology", "Ecology", "Biotechnology", "Cellular"],
    "earth_inc": ["Geology", "Cosmology", "Tectonics", "Petrology", "Oceanography"]
}

def analyze_title(title):
    title_upper = str(title).upper()
    
    # أولوية 1: البيطرة
    for word in keywords["vet_inc"]:
        if word.upper() in title_upper: return t["dec_acc_vet"], t["vet_title"]
        
    # أولوية 2: استبعاد الطب السريري
    for word in keywords["med_ex"]:
        if word.upper() in title_upper: return t["dec_rej_clin"], "-"
        
    # أولوية 3: الطب الأساسي
    for word in keywords["med_inc"]:
        if word.upper() in title_upper: return t["dec_acc_med"], t["med_title"]
        
    # أولوية 4: البيولوجيا
    for word in keywords["bio_inc"]:
        if word.upper() in title_upper: return t["dec_acc_bio"], t["bio_title"]
        
    # أولوية 5: علوم الأرض
    for word in keywords["earth_inc"]:
        if word.upper() in title_upper: return t["dec_acc_earth"], t["earth_title"]
        
    return t["dec_out"], "-"

# 5. الواجهة والتصميم
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        .main-container {{ direction: {t['dir']}; text-align: {'right' if lang == 'AR' else 'left'}; font-family: 'Cairo', sans-serif; }}
        div.stApp::before {{
            content: "منصة من تصميم الأستاذ: جلابي بلال";
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-25deg);
            font-size: 45px; font-weight: 700; color: rgba(0, 43, 91, 0.04); 
            white-space: nowrap; pointer-events: none; z-index: -100; font-family: 'Cairo', sans-serif;
        }}
        .main-header {{
            background: linear-gradient(90deg, #001b3d 0%, #00cfb2 100%); color: white; 
            padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; direction: {t['dir']};
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-container">', unsafe_allow_html=True)
st.markdown(f'<div class="main-header"><h1>{t["title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)

st.subheader(t["upload_title"])
uploaded_file = st.file_uploader("", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # محاولة العثور على العمود بذكاء
    possible_names = ['العنوان', 'عنوان', 'Title', 'title', 'Titre', 'titre', 'Subject', 'Designation', 'الكتاب']
    detected_col = next((c for c in df.columns if any(p.lower() in str(c).lower() for p in possible_names)), None)
    
    # إذا لم يجده، يظهر قائمة منسدلة ليختار منها المستخدم
    final_col = detected_col if detected_col else st.selectbox(t["select_col"], df.columns)

    if final_col:
        with st.spinner(t["processing"]):
            df[['Decision', 'Dept']] = df.apply(lambda row: pd.Series(analyze_title(row[final_col])), axis=1)
            
            total = len(df); acc = len(df[df['Decision'].str.contains('🟢')])
            rej = total - acc
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t["total_books"], total)
            c2.metric(t["accepted"], acc)
            c3.metric(t["rejected"], rej)
            
            st.dataframe(df, use_container_width=True)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(t["download_btn"], buffer.getvalue(), "Muashir_Report.xlsx")

st.sidebar.markdown(f"--- \n **{t['sig']}**")
st.markdown('</div>', unsafe_allow_html=True)