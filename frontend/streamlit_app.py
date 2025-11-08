import streamlit as st
import requests
import os
from datetime import datetime

# Config
API_URL = os.getenv("BACKEND_URL", "https://0ac6237c043a.ngrok-free.app")
CHAT_ENDPOINT = f"{API_URL}/chat"

# Page configuration
st.set_page_config(
    page_title="Interior Design Assistant",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 0 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background: #f0f2f6;
        color: #262730;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0;
        margin: 8px 0;
        max-width: 80%;
        text-align: left;
        border: 1px solid #e6e6e6;
    }
    .chat-container {
        height: 600px;
        overflow-y: auto;
        padding: 20px;
        border: 1px solid #e6e6e6;
        border-radius: 15px;
        margin-bottom: 20px;
        background: white;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    .design-tips {
        background: #e8f4fd;
        padding: 15px;
        border-radius: 10px;
        border-right: 4px solid #667eea;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

def send_message(user_message: str):
    """Send message to backend and handle response"""
    payload = {"message": user_message, "history": st.session_state.history}
    try:
        with st.spinner("🔄 جاري تحليل طلبك وإعداد الاقتراحات..."):
            r = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            reply = data.get("reply", "")
            
            # Append to history with timestamp
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": timestamp
            })
            st.session_state.history.append({
                "role": "assistant", 
                "content": reply,
                "timestamp": timestamp
            })
            
            # Clear input after successful send
            st.session_state.current_input = ""
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ خطأ في الاتصال: {str(e)}")
    except Exception as e:
        st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")

def clear_chat():
    """Clear chat history"""
    st.session_state.history = []
    st.session_state.current_input = ""

def export_chat():
    """Export chat history to text file"""
    if st.session_state.history:
        chat_text = "Interior Design Chat History\n"
        chat_text += "=" * 30 + "\n\n"
        
        for msg in st.session_state.history:
            role = "You" if msg["role"] == "user" else "Design Assistant"
            chat_text += f"{role} ({msg.get('timestamp', '')}):\n"
            chat_text += f"{msg['content']}\n"
            chat_text += "-" * 50 + "\n"
        
        return chat_text
    return ""

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 أدوات التصميم")
    
    st.markdown("#### 💡 نصائح سريعة")
    st.markdown("""
    <div class="design-tips">
    • اذكر أبعاد الغرفة (الطول × العرض × الارتفاع)<br>
    • حدد اتجاه النوافذ والإضاءة الطبيعية<br>
    • اختر نمط التصميم المفضل<br>
    • حدد الميزانية التقريبية<br>
    • اذكر الألوان المفضلة<br>
    • اذكر عدد الأشخاص المستخدمين للغرفة
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🏠 أنماط التصميم")
    design_styles = [
        "🏛️ كلاسيكي", "🔄 مودرن", "🌿 مينيمالست", 
        "🇸🇪 سكاندينيفيان", "🏭 صناعي", "🏖️ ساحلي",
        "🌾 ريفي", "🎨 بوهو", "🌏 آسيوي"
    ]
    
    for style in design_styles:
        st.write(f"• {style}")
    
    st.markdown("---")
    
    # Chat management
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            clear_chat()
            st.rerun()
    
    with col2:
        chat_text = export_chat()
        if chat_text:
            st.download_button(
                label="📥 حفظ المحادثة",
                data=chat_text,
                file_name=f"design_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# Main content
st.markdown('<div class="main-header"><h1>🛋️ مساعد التصميم الداخلي</h1><p>اسأل عن تصميم غرفتك - اكتب بالعربية أو الإنجليزية</p></div>', unsafe_allow_html=True)

# Chat container
with st.container():
    st.markdown("### 💬 محادثة التصميم")
    
    # Chat messages display
    chat_container = st.container()
    with chat_container:
        if st.session_state.history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for msg in st.session_state.history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <div style="font-size: 0.8em; opacity: 0.8;">أنت • {msg.get('timestamp', '')}</div>
                        {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <div style="font-size: 0.8em; opacity: 0.8;">المساعد • {msg.get('timestamp', '')}</div>
                        {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Auto scroll to bottom
            st.markdown("""
            <script>
                var chatContainer = window.parent.document.querySelector('.chat-container');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            </script>
            """, unsafe_allow_html=True)
        else:
            # Welcome message when no chat history
            st.markdown("""
            <div style="text-align: center; padding: 40px; color: #666;">
                <h3>🎉 أهلاً بك في مساعد التصميم الداخلي!</h3>
                <p>ابدأ بوصف غرفتك وسأساعدك في تصميمها بشكل احترافي</p>
                <p>💡 استخدم الشريط الجانبي للحصول على نصائح سريعة</p>
            </div>
            """, unsafe_allow_html=True)

# Input area
st.markdown("### ✍️ اكتب وصف الغرفة")

input_col1, input_col2 = st.columns([4, 1])
with input_col1:
    user_input = st.text_area(
        "وصف الغرفة:",
        value=st.session_state.current_input,
        height=120,
        placeholder="مثال: لدي غرفة معيشة 4×5 متر، بها نافذة كبيرة اتجاه الشمال، أريد تصميم مودرن بميزانية متوسطة...",
        label_visibility="collapsed"
    )

with input_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    send_button = st.button("🚀 إرسال", use_container_width=True, type="primary")

# Quick suggestion buttons
st.markdown("#### 💡 اقتراحات سريعة")
quick_cols = st.columns(4)
quick_suggestions = [
    "تصميم غرفة معيشة 4×5 متر",
    "ألوان مناسبة لغرفة نوم",
    "ديكور مودرن لمكتب صغير", 
    "ترتيب أثاث غرفة مستطيلة"
]

for col, suggestion in zip(quick_cols, quick_suggestions):
    with col:
        if st.button(suggestion, use_container_width=True):
            st.session_state.current_input = suggestion
            st.rerun()

# Handle send action
if send_button and user_input.strip():
    send_message(user_input.strip())
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>🛋️ مساعد التصميم الداخلي - قدم وصفاً دقيقاً للحصول على أفضل النتائج</p>
</div>
""", unsafe_allow_html=True)
