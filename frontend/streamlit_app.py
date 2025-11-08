import streamlit as st
import requests
import json
import time

# إعداد الصفحة الأساسية
st.set_page_config(
    page_title="نظام التصميم الداخلي",
    page_icon="🏠",
    layout="wide"
)

# CSS مخصص بسيط
st.markdown("""
<style>
    .arabic-text {
        text-align: right;
        direction: rtl;
    }
    .header {
        color: #2E86AB;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        color: #666;
        margin-top: 3rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="header">🎨 نظام التصميم الداخلي الذكي</div>', unsafe_allow_html=True)

# معلومات الاتصال
API_URL = "https://pausal-inexpertly-ernesto.ngrok-free.dev"
API_KEY = "secret123"

# التحقق من اتصال السيرفر
def check_server_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        return response.status_code == 200
    except:
        return False

# عرض حالة السيرفر
server_status = check_server_health()
if server_status:
    st.success("✅ السيرفر متصل ويعمل بشكل طبيعي")
else:
    st.error("❌ لا يمكن الاتصال بالسيرفر - تأكد من تشغيله")

# التبويبات الرئيسية
tab1, tab2 = st.tabs(["🏠 تصميم الغرف", "📝 توليد النصوص"])

with tab1:
    st.markdown("### تصميم الغرفة والديكور")
    
    # نموذج إدخال البيانات
    col1, col2 = st.columns(2)
    
    with col1:
        room_type = st.selectbox(
            "نوع الغرفة",
            ["غرفة معيشة", "غرفة نوم", "مطبخ", "غرفة طعام", "غرفة أطفال"]
        )
        
        room_size = st.text_input("المساحة", "٦×٤ متر")
        
    with col2:
        budget = st.selectbox(
            "الميزانية",
            ["محدودة", "متوسطة", "مرتفعة"]
        )
        
        style_preference = st.selectbox(
            "النمط المفضل", 
            ["مودرن", "كلاسيكي", "مينيمالست", "سكاندينيفيان", "أي نمط"]
        )
    
    additional_requirements = st.text_area("المتطلبات الإضافية", placeholder="أوصي متطلباتك الخاصة هنا...")

    if st.button("🎨 إنشاء التصميم", type="primary"):
        if not all([room_type, room_size, budget]):
            st.warning("⚠️ يرجى ملء جميع الحقول الإلزامية")
        else:
            with st.spinner("جاري إنشاء التصميم المثالي..."):
                try:
                    data = {
                        "room_type": room_type,
                        "room_size": room_size,
                        "budget": budget,
                        "style_preference": style_preference,
                        "additional_requirements": additional_requirements
                    }
                    
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    response = requests.post(
                        f"{API_URL}/design", 
                        json=data, 
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # عرض النتيجة
                        st.success("✅ تم إنشاء التصميم بنجاح!")
                        st.markdown("### 📋 التصميم المقترح:")
                        
                        # تقسيم النص لعرض أفضل
                        design_text = result.get('design_recommendations', '')
                        paragraphs = design_text.split('\n\n')
                        
                        for paragraph in paragraphs:
                            if paragraph.strip():
                                st.markdown(f'<div class="arabic-text">{paragraph}</div>', unsafe_allow_html=True)
                                st.markdown("---")
                        
                        # زر التحميل
                        st.download_button(
                            label="📥 تحميل التصميم",
                            data=design_text,
                            file_name=f"تصميم_{room_type}.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        st.error(f"❌ خطأ من السيرفر: {response.status_code}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏰ انتهت مهلة الانتظار - حاول مرة أخرى")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 خطأ في الاتصال - تأكد من تشغيل السيرفر")
                except Exception as e:
                    st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")

with tab2:
    st.markdown("### توليد النصوص الذكي")
    
    prompt = st.text_area(
        "اكتب طلبك هنا",
        placeholder="اكتب موضوعك أو سؤالك هنا...",
        height=100
    )
    
    max_length = st.slider("الطول الأقصى", 100, 1000, 300)
    
    if st.button("🪄 توليد النص", type="primary"):
        if not prompt:
            st.warning("⚠️ يرجى كتابة prompt")
        else:
            with st.spinner("جاري توليد النص..."):
                try:
                    data = {
                        "prompt": prompt,
                        "max_length": max_length
                    }
                    
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    response = requests.post(
                        f"{API_URL}/generate", 
                        json=data, 
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ تم توليد النص بنجاح!")
                        
                        st.markdown("### 📖 النص المُولد:")
                        generated_text = result.get('generated_text', '')
                        st.markdown(f'<div class="arabic-text">{generated_text}</div>', unsafe_allow_html=True)
                        
                        # زر التحميل
                        st.download_button(
                            label="📥 تحميل النص",
                            data=generated_text,
                            file_name="نص_مولد.txt",
                            mime="text/plain"
                        )
                        
                    else:
                        st.error(f"❌ خطأ من السيرفر: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")

# معلومات المساعدة
with st.expander("🆘 المساعدة والدعم"):
    st.markdown("""
    ### 📋 إرشادات الاستخدام:
    
    1. **تصميم الغرف**: اختر نوع الغرفة واملأ البيانات الأساسية
    2. **توليد النصوص**: اكتب أي موضوع لتحصل على نص مخصص
    3. **تحميل النتائج**: يمكنك تحميل أي نتيجة كملف نصي
    
    ### 🔧 استكشاف الأخطاء:
    - تأكد من تشغيل السيرفر الأساسي
    - تحقق من اتصال الإنترنت
    - إذا استمرت المشكلة، جرب تحديث الصفحة
    """)

# التذييل
st.markdown("---")
st.markdown(
    '<div class="footer">'
    'تم التطوير بواسطة <strong>Eng. Youssef Abdelnasser</strong> | '
    'جميع الحقوق محفوظة 2024'
    '</div>',
    unsafe_allow_html=True
)
