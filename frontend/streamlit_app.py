import streamlit as st
import requests
import json
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="نظام التصميم الداخلي الذكي",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم باستخدام CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: right;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        text-align: right;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .design-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: right;
    }
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: right;
    }
    .footer {
        text-align: left;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 2px solid #2E86AB;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E86AB 0%, #A23B72 100%);
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<h1 class="main-header">🎨 نظام التصميم الداخلي الذكي</h1>', unsafe_allow_html=True)

# معلومات السيرفر (يجب تعديلها حسب عنوانك)
API_URL = "https://pausal-inexpertly-ernesto.ngrok-free.dev"
API_KEY = "secret123"

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    st.info("**السيرفر:** يعمل بنجاح ✅")
    st.info(f"**الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات النظام")
    if 'request_count' not in st.session_state:
        st.session_state.request_count = 0
    st.metric("عدد الطلبات", st.session_state.request_count)
    
    st.markdown("---")
    st.markdown("### 🎯 التعليمات")
    st.write("""
    1. اختر نوع الخدمة
    2. املأ البيانات المطلوبة
    3. اضغط على زر التشغيل
    4. انتظر النتائج
    """)

# تبويبات الخدمات
tab1, tab2, tab3 = st.tabs(["🏠 تصميم الغرف", "📝 توليد النصوص", "ℹ️ معلومات النظام"])

with tab1:
    st.markdown('<h2 class="sub-header">تصميم الغرف والديكور</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        room_type = st.selectbox(
            "نوع الغرفة 🏠",
            ["غرفة معيشة", "غرفة نوم", "مطبخ", "غرفة طعام", "غرفة أطفال", "حمام", "غرفة دراسة"]
        )
        
        room_size = st.text_input("المساحة بالمتر 📏", "٦×٤ متر")
        
        budget = st.selectbox(
            "الميزانية 💰",
            ["محدودة", "متوسطة", "مرتفعة", "فاخرة"]
        )
    
    with col2:
        style_preference = st.selectbox(
            "النمط المفضل 🎭",
            ["مودرن", "كلاسيكي", "مينيمالست", "سكاندينيفيان", "صناعي", "بوهو", "ريفي", "أي نمط"]
        )
        
        additional_requirements = st.text_area(
            "المتطلبات الإضافية 📝",
            "مساحة مريحة، إضاءة جيدة، تخزين عملي"
        )
    
    if st.button("🎨 إنشاء التصميم", use_container_width=True):
        if room_type and room_size and budget:
            with st.spinner("جاري إنشاء التصميم المثالي لك..."):
                try:
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "room_type": room_type,
                        "room_size": room_size,
                        "budget": budget,
                        "style_preference": style_preference,
                        "additional_requirements": additional_requirements
                    }
                    
                    response = requests.post(f"{API_URL}/design", headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.request_count += 1
                        
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown(f"### 🎯 تصميم {room_type}")
                        st.markdown("---")
                        st.markdown(result['design_recommendations'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # تحميل النتيجة
                        st.download_button(
                            label="📥 تحميل التصميم",
                            data=result['design_recommendations'],
                            file_name=f"تصميم_{room_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"خطأ في السيرفر: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى ملء جميع الحقول المطلوبة")

with tab2:
    st.markdown('<h2 class="sub-header">توليد النصوص الذكي</h2>', unsafe_allow_html=True)
    
    prompt = st.text_area(
        "اكتب طلبك هنا ✍️",
        "اكتب عن أهمية التصميم الداخلي في تحسين جودة الحياة...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    with col1:
        max_length = st.slider("الطول الأقصى للنص", 100, 2000, 500)
    
    if st.button("🪄 توليد النص", use_container_width=True):
        if prompt:
            with st.spinner("جاري توليد النص..."):
                try:
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "prompt": prompt,
                        "max_length": max_length
                    }
                    
                    response = requests.post(f"{API_URL}/generate", headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.request_count += 1
                        
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown("### 📖 النص المُولد")
                        st.markdown("---")
                        st.markdown(result['generated_text'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # تحميل النص
                        st.download_button(
                            label="📥 تحميل النص",
                            data=result['generated_text'],
                            file_name=f"نص_مولد_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"خطأ في السيرفر: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى كتابة prompt")

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="design-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 معلومات النظام")
        st.markdown("""
        - **النموذج:** Mistral-Nemo-Instruct
        - **اللغة:** العربية
        - **الخدمات:** تصميم داخلي + توليد نصوص
        - **الحالة:** 🟢 نشط
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="design-card">', unsafe_allow_html=True)
        st.markdown("### 💡 نصائح سريعة")
        st.markdown("""
        - كن محدداً في وصف المتطلبات
        - اختر الميزانية المناسبة
        - اذكر الاستخدام اليومي للغرفة
        - حدد الألوان المفضلة إذا أمكن
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="design-card">', unsafe_allow_html=True)
        st.markdown("### 🎭 أنماط التصميم")
        st.markdown("""
        - **مودرن:** خطوط نظيفة، ألوان محايدة
        - **كلاسيكي:** تفاصيل فاخرة، ألوان دافئة
        - **مينيمالست:** بساطة، مساحات مفتوحة
        - **سكاندينيفيان:** فاتح، طبيعي، عملي
        - **صناعي:** خام، معدني، مكشوف
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # زر فحص الحالة
        if st.button("🔍 فحص حالة السيرفر", use_container_width=True):
            try:
                response = requests.get(f"{API_URL}/health")
                if response.status_code == 200:
                    st.success("✅ السيرفر يعمل بشكل طبيعي")
                    st.json(response.json())
                else:
                    st.error("❌ هناك مشكلة في السيرفر")
            except:
                st.error("❌ لا يمكن الوصول إلى السيرفر")

# التذييل
st.markdown("---")
st.markdown(
    '<div class="footer">'
    'تم التطوير بواسطة <strong>Eng. Youssef Abdelnasser</strong> 🚀 | '
    'نظام التصميم الداخلي الذكي'
    '</div>',
    unsafe_allow_html=True
)

# تأثيرات إضافية
st.balloons()
