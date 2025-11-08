import streamlit as st
import requests
from streamlit_chat import message

# ===============================
# 🔧 إعدادات التطبيق
# ===============================
API_URL = "https://pausal-inexpertly-ernesto.ngrok-free.dev"
API_KEY = "secret123"

st.set_page_config(page_title="Interior Design Chatbot", page_icon="🎨", layout="wide")

# ===============================
# 🎨 تصميم الواجهة
# ===============================
st.markdown("""
    <style>
        body {
            background-color: #f5f6fa;
        }
        .stApp {
            background: linear-gradient(180deg, #f9fafc 0%, #e9eff8 100%);
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            color: #3b3b98;
        }
        .sub {
            text-align: center;
            color: #718093;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .stTextInput>div>div>input {
            border-radius: 12px;
            border: 1px solid #dcdde1;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏠 Interior Design AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>تحدث مع المساعد الذكي للحصول على أفكار وتصميمات داخلية مذهلة!</p>", unsafe_allow_html=True)

# ===============================
# 💬 سجل المحادثة
# ===============================
if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# 🚀 واجهة المستخدم
# ===============================
with st.container():
    user_input = st.text_input("💬 اكتب سؤالك هنا:", placeholder="مثال: أريد تصميم غرفة نوم مودرن بألوان هادئة...", key="input")

    col1, col2 = st.columns([1, 5])
    with col1:
        send_btn = st.button("🔍 أرسل")

# ===============================
# ⚙️ وظائف التواصل مع الـ API
# ===============================
def generate_response(prompt):
    """ترسل الطلب إلى الـ backend"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.post(f"{API_URL}/generate", json={"prompt": prompt}, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "لم يتم استلام رد من الخادم.")
        else:
            return f"⚠️ خطأ من الخادم: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ فشل الاتصال بالخادم: {e}"

# ===============================
# 💡 تنفيذ المحادثة
# ===============================
if send_btn and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    bot_reply = generate_response(user_input)
    st.session_state.history.append({"role": "assistant", "content": bot_reply})

# ===============================
# 💬 عرض المحادثة
# ===============================
for chat in st.session_state.history:
    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=chat["content"] + "_user")
    else:
        message(chat["content"], key=chat["content"] + "_bot")

