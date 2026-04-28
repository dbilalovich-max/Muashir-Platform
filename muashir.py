import streamlit as st
import pandas as pd
import io

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="منصة مؤشر | Muashir Platform", layout="wide", page_icon="📚")

# 2. القاموس اللغوي
translations = {
    "AR": {
        "title": "📚 منصة \"مؤشر\" للتحليل الذكي للفهارس",
        "subtitle": "مكتبة الكلية - جامعة 8 ماي 1945 قالمة",
        "upload_title": "📁 مساحة العمل: رفع قائمة المورد",
        "select_col": "⚠️ لم أتعرف على عمود العناوين تلقائياً، يرجى اختياره من القائمة:",
        "processing": "جاري التحليل...",
        "total_books": "📚 إجمالي الكتب", "accepted": "✅ مطابقة", "rejected": "❌ مستبعدة",
        "download_btn": "📥 تصدير النتائج (Excel)",
        "sig": "منصة من تصميم: جلابي بلال", "dir": "rtl"
    },
    "EN": {
        "title": "📚 'Muashir' Smart Analysis",
        "subtitle": "Faculty Library - University of 8 Mai 1945 Guelma",
        "upload_title": "📁 Workspace: Upload Supplier List",
        "select_col": "⚠️ Could not auto-detect the Title column. Please select it:",
        "processing": "Analyzing...",
        "total_books": "📚 Total Books", "accepted": "✅ Accepted", "rejected": "❌ Rejected",
        "download_btn": "📥 Export to Excel",
        "sig": "Success Partner: DJELLABI Bilal", "dir": "ltr"
    },
    "ZH": {
        "title": "📚 “Muashir” 智能分析",
        "subtitle": "Faculty Library - University of 8 Mai 1945 Guelma",
        "upload_title": "📁 工作区：上传清单",
        "select_col": "⚠️ 无法自动识别标题列，请手动选择：",
        "processing": "分析中...",
        "total_books": "📚 总数", "accepted": "✅ 已接受", "rejected": "❌ 已拒绝",
        "download_btn": "📥 导出 Excel",
        "sig": "合作伙伴：DJELLABI Bilal", "dir": "ltr"
    }
}

st.sidebar.title("🌐 Language")
lang_choice = st.sidebar.radio("", ["العربية", "English", "中文"])
lang = "AR" if lang_choice == "العربية" else ("EN" if lang_choice == "English" else "ZH")
t = translations[lang]

# 3. محرك الفلترة (الكلمات المفتاحية)
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
        if word.upper() in title_upper: return "❌ Rejected (Clinical)", "-"
    for word in keywords["med_inc"]:
        if word.upper() in title_upper: return "✅ Accepted (Medical)", "Medicine"
    for word in keywords["bio_inc"]:
        if word.upper() in title_upper: return "✅ Accepted (Biology)", "Biology"
    for word in keywords["earth_inc"]:
        if word.upper() in title_upper: return "✅ Accepted (Earth)", "Earth Sciences"
    for word in keywords["vet_inc"]:
        if word.upper() in title_upper: return "✅ Accepted (Vet)", "Veterinary"
    return "⚪ Out of Scope", "-"

# 4. واجهة المستخدم
st.markdown(f"""<style>.main-header {{ background: linear-gradient(90deg, #001b3d 0%, #00cfb2 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; direction: {t['dir']}; }}</style>""", unsafe_allow_html=True)
st.markdown(f'<div class="main-header"><h1>{t["title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(t["upload_title"], type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # خوارزمية البحث الذكي عن العمود (Fuzzy Search)
    possible_names = ['العنوان', 'عنوان', 'Title', 'title', 'Titre', 'titre', 'Subject', 'Designation', 'الكتاب']
    detected_col = next((c for c in df.columns if any(p.lower() in str(c).lower() for p in possible_names)), None)
    
    final_col = None
    if detected_col:
        final_col = detected_col
    else:
        # إذا لم يجد شيئاً، يطلب من المستخدم الاختيار
        final_col = st.selectbox(t["select_col"], df.columns)

    if final_col:
        with st.spinner(t["processing"]):
            df[['Decision', 'Dept']] = df.apply(lambda row: pd.Series(analyze_title(row[final_col])), axis=1)
            
            total = len(df); acc = len(df[df['Decision'].str.contains('✅')]); rej = total - acc
            c1, c2, c3 = st.columns(3)
            c1.metric(t["total_books"], total)
            c2.metric(t["accepted"], acc)
            c3.metric(t["rejected"], rej)
            
            st.dataframe(df, use_container_width=True)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(t["download_btn"], buffer.getvalue(), "Muashir_Report.xlsx")

st.sidebar.markdown(f"--- \n {t['sig']}")