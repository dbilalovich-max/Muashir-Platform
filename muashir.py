import streamlit as st
import pandas as pd
import io

# 1. إعدادات الهوية البصرية (بدون إجبار يكسر الواجهة)
st.set_page_config(page_title="منصة مؤشر | Muashir Platform", layout="wide", page_icon="📚")

# 2. القاموس اللغوي الشامل (ترجمة دقيقة 100% ومتزامنة)
translations = {
    "AR": {
        "title": "📚 منصة \"مؤشر\" للتحليل الذكي للفهارس",
        "subtitle": "المكتبة المركزية - جامعة 8 ماي 1945 قالمة",
        "med_title": "الملحقة الطبية", "med_desc": "العلوم الأساسية",
        "bio_title": "علوم الطبيعة والحياة", "bio_desc": "البيولوجيا والبيئة",
        "earth_title": "علوم الأرض والكون", "earth_desc": "الجيولوجيا والفلك",
        "vet_title": "العلوم البيطرية", "vet_desc": "التشريح والأمراض",
        "upload_title": "📁 مساحة العمل: رفع قائمة المورد",
        "upload_help": "قم بإسقاط ملف الإكسل (Excel) هنا لتبدأ عملية الفلترة الذكية...",
        "processing": "يتم الآن فحص العناوين وتوجيهها...",
        "total_books": "📚 إجمالي الكتب الواردة",
        "accepted": "✅ عناوين مطابقة",
        "rejected": "❌ عناوين مستبعدة",
        "report_title": "📊 تقرير الفلترة التفصيلي",
        "download_btn": "📥 تصدير النتائج بصيغة Excel",
        "error_msg": "تنبيه: لم يتم العثور على عمود باسم 'العنوان' أو 'Title'.",
        "sig": "شريك النجاح: جلابي بلال",
        "dir": "rtl",
        # نتائج الفلترة
        "dec_rej_clin": "مستبعد 🔴 (سريري)", "dec_acc_med": "قبول 🟢 (طب)",
        "dec_acc_bio": "قبول 🟢 (بيولوجيا)", "dec_acc_earth": "قبول 🟢 (أرض)",
        "dec_acc_vet": "قبول 🟢 (بيطرة)", "dec_out": "مستبعد ⚪ (خارج النطاق)"
    },
    "EN": {
        "title": "📚 'Muashir' Smart Catalog Analysis Platform",
        "subtitle": "Central Library - University of 8 Mai 1945 Guelma",
        "med_title": "Medical Annex", "med_desc": "Basic Sciences",
        "bio_title": "Nature & Life Sciences", "bio_desc": "Biology & Environment",
        "earth_title": "Earth & Universe Sciences", "earth_desc": "Geology & Astronomy",
        "vet_title": "Veterinary Sciences", "vet_desc": "Anatomy & Pathology",
        "upload_title": "📁 Workspace: Upload Supplier List",
        "upload_help": "Drop the Excel file here to start the smart filtering process...",
        "processing": "Analyzing and routing titles...",
        "total_books": "📚 Total Incoming Books",
        "accepted": "✅ Matching Titles",
        "rejected": "❌ Auto-Rejected Titles",
        "report_title": "📊 Detailed Filtering Report",
        "download_btn": "📥 Export Results as Excel",
        "error_msg": "Alert: Could not find a column named 'Title' or 'العنوان'.",
        "sig": "Success Partner: Jellabi Bilal",
        "dir": "ltr",
        # Filtering Results
        "dec_rej_clin": "Rejected 🔴 (Clinical)", "dec_acc_med": "Accepted 🟢 (Medicine)",
        "dec_acc_bio": "Accepted 🟢 (Biology)", "dec_acc_earth": "Accepted 🟢 (Earth Sci)",
        "dec_acc_vet": "Accepted 🟢 (Veterinary)", "dec_out": "Rejected ⚪ (Out of Scope)"
    },
    "ZH": {
        "title": "📚 “Muashir” 智能书目分析平台",
        "subtitle": "中央图书馆 - 1945年5月8日盖尔马大学",
        "med_title": "医学附属学院", "med_desc": "基础科学",
        "bio_title": "自然与生命科学", "bio_desc": "生物与环境",
        "earth_title": "地球与宇宙科学", "earth_desc": "地质与天文学",
        "vet_title": "兽医学", "vet_desc": "解剖与病理学",
        "upload_title": "📁 工作区：上传供应商清单",
        "upload_help": "将Excel文件拖放到此处以启动智能过滤过程...",
        "processing": "正在分析和路由标题...",
        "total_books": "📚 接收书籍总数",
        "accepted": "✅ 符合教学大纲的标题",
        "rejected": "❌ 自动拒绝的标题",
        "report_title": "📊 详细过滤报告",
        "download_btn": "📥 导出结果为Excel",
        "error_msg": "警告：找不到名为“Title”或“العنوان”的列。",
        "sig": "成功合作伙伴：Jellabi Bilal",
        "dir": "ltr",
        # Filtering Results
        "dec_rej_clin": "拒绝 🔴 (临床)", "dec_acc_med": "接受 🟢 (医学)",
        "dec_acc_bio": "接受 🟢 (生物学)", "dec_acc_earth": "接受 🟢 (地球科学)",
        "dec_acc_vet": "接受 🟢 (兽医学)", "dec_out": "拒绝 ⚪ (超出范围)"
    }
}

# 3. اختيار اللغة من القائمة الجانبية
st.sidebar.title("🌐 Language / اللغة / 语言")
lang_choice = st.sidebar.radio("", ["العربية", "English", "中文"])
if lang_choice == "العربية": lang = "AR"
elif lang_choice == "English": lang = "EN"
else: lang = "ZH"

t = translations[lang] # استدعاء القاموس حسب اللغة المحددة

# 4. التنسيقات (CSS) الآمنة التي لا تكسر الواجهة
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* تطبيق الاتجاه ديناميكياً بناء على اللغة دون المساس بأدوات الرفع */
        .main-container {{
            direction: {t['dir']};
            text-align: {'right' if lang == 'AR' else 'left'};
            font-family: 'Cairo', sans-serif;
        }}
        
        /* التوقيع المائي في الخلفية */
        div.stApp::before {{
            content: "شريكك الاستراتيجي في بناء منصات النجاح: جلابي بلال";
            position: fixed; top: 50%; left: 50%;
            transform: translate(-50%, -50%) rotate(-25deg);
            font-size: 45px; font-weight: 700; color: rgba(0, 43, 91, 0.04); 
            white-space: nowrap; pointer-events: none; z-index: -100; font-family: 'Cairo', sans-serif;
        }}
        
        /* التوقيع النصي السفلي */
        .personal-sig {{
            position: fixed; bottom: 10px; {'left' if lang != 'AR' else 'right'}: 10px; font-size: 14px;
            color: rgba(0, 43, 91, 0.6); background-color: rgba(255, 255, 255, 0.8);
            padding: 5px 15px; border-radius: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 1000;
        }}

        /* رأس الصفحة */
        .main-header {{
            background: linear-gradient(90deg, #001b3d 0%, #00cfb2 100%);
            color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;
            text-align: center; box-shadow: 0 10px 20px rgba(0,207,178,0.2); direction: {t['dir']};
        }}
        
        /* بطاقات التخصصات */
        .faculty-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
            border: 1px solid #00cfb2; border-radius: 12px; padding: 15px;
            text-align: center; font-weight: bold; color: #001b3d;
            height: 100%; transition: transform 0.3s ease; direction: {t['dir']};
        }}
        .faculty-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,207,178,0.15); }}
        .fac-icon {{ font-size: 35px; margin-bottom: 10px; display: block; }}
    </style>
""", unsafe_allow_html=True)

# 5. بناء الواجهة بناءً على اللغة المختارة
st.markdown(f'<div class="main-container">', unsafe_allow_html=True)

# رأس الصفحة
st.markdown(f'<div class="main-header"><h1>{t["title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)

# شريط الكليات
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='faculty-card'><span class='fac-icon'>🩺</span>{t['med_title']}<br><small>{t['med_desc']}</small></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='faculty-card'><span class='fac-icon'>🧬</span>{t['bio_title']}<br><small>{t['bio_desc']}</small></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='faculty-card'><span class='fac-icon'>🌍</span>{t['earth_title']}<br><small>{t['earth_desc']}</small></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='faculty-card'><span class='fac-icon'>🐾</span>{t['vet_title']}<br><small>{t['vet_desc']}</small></div>", unsafe_allow_html=True)

st.write(""); st.divider()
st.markdown(f'<div class="personal-sig"><i class="fa-solid fa-code"></i> {t["sig"]}</div>', unsafe_allow_html=True)

# 6. محرك الفلترة الذكي (يعمل باللغات المتعددة)
keywords = {
    "med_ex": ["Surgery", "Pediatrics", "Obstetrics", "Internal Medicine"],
    "med_inc": ["Anatomy", "Physiology", "Pathology", "Biochemistry", "Pharmacology", "Histology"],
    "bio_inc": ["Biology", "Genetics", "Microbiology", "Ecology", "Biotechnology", "Cellular"],
    "earth_inc": ["Geology", "Cosmology", "Tectonics", "Petrology", "Oceanography"],
    "vet_inc": ["Veterinary", "Animal Anatomy", "Zoonotic", "Dyce", "الطفيليات البيطرية"]
}

def analyze_title(title):
    title_upper = str(title).upper()
    for word in keywords["med_ex"]:
        if word.upper() in title_upper: return t["dec_rej_clin"], "-"
    for word in keywords["med_inc"]:
        if word.upper() in title_upper: return t["dec_acc_med"], t["med_title"]
    for word in keywords["bio_inc"]:
        if word.upper() in title_upper: return t["dec_acc_bio"], t["bio_title"]
    for word in keywords["earth_inc"]:
        if word.upper() in title_upper: return t["dec_acc_earth"], t["earth_title"]
    for word in keywords["vet_inc"]:
        if word.upper() in title_upper: return t["dec_acc_vet"], t["vet_title"]
    return t["dec_out"], "-"

# 7. مساحة الرفع والنتائج
st.subheader(t["upload_title"])
uploaded_file = st.file_uploader(t["upload_help"], type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    cols = [c for c in df.columns if 'Title' in str(c) or 'العنوان' in str(c) or 'title' in str(c)]
    
    if cols:
        title_col = cols[0]
        with st.spinner(t["processing"]):
            df['Smart Decision'] = ""
            df['Department'] = ""
            
            # تطبيق الفلترة واسترجاع النتائج المترجمة
            results = df.apply(lambda row: pd.Series(analyze_title(row[title_col])), axis=1)
            df['Smart Decision'] = results[0]
            df['Department'] = results[1]
            
            total = len(df); acc = len(df[df['Smart Decision'].str.contains('🟢')])
            rej = total - acc
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t["total_books"], total)
            c2.metric(t["accepted"], acc)
            c3.metric(t["rejected"], rej)
            
            st.divider(); st.subheader(t["report_title"])
            st.dataframe(df, use_container_width=True)
            
            # التصدير
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Filtered_Results')
            st.download_button(label=t["download_btn"], data=buffer.getvalue(),
                               file_name="Muashir_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error(t["error_msg"])

st.markdown('</div>', unsafe_allow_html=True)