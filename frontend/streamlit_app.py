# frontend/streamlit_app.py
import streamlit as st
import requests
import os

# Config
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # use BACKEND_URL env var in deployment
CHAT_ENDPOINT = f"{API_URL}/chat"

st.set_page_config(page_title="Interior Design Chatbot", layout="centered")

st.title("🛋️ Interior Design Chatbot")
st.write("اسأل مساعد الديكور عن تصميم غرفتك — اكتب بالعربي أو بالإنجليزي.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "...", "content": "..."}

def send_message(user_message: str):
    payload = {"message": user_message, "history": st.session_state.history}
    try:
        with st.spinner("جاري الحصول على اقتراح..."):
            r = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            reply = data.get("reply", "")
            # Append messages to history
            st.session_state.history.append({"role": "user", "content": user_message})
            st.session_state.history.append({"role": "assistant", "content": reply})
    except requests.exceptions.RequestException as e:
        st.error("خطأ في الاتصال بالباك إند: " + str(e))
    except Exception as e:
        st.error("حدث خطأ: " + str(e))

# Display chat history
def render_chat():
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right; background:#E8F0FF; padding:8px; border-radius:8px'>"
                        f"<b>أنت:</b> {st.markdown(msg['content'], unsafe_allow_html=True) or ''}</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background:#F5F5F5; padding:8px; border-radius:8px'>"
                        f"<b>المساعد:</b><br>{msg['content']}</div>",
                        unsafe_allow_html=True)

# Input area
with st.form(key="chat_form", clear_on_submit=False):
    user_input = st.text_area("اكتب وصف غرفتك أو اسأل:", height=120)
    submit = st.form_submit_button("أرسل")

if submit and user_input.strip() != "":
    send_message(user_input.strip())

# Show history
if st.session_state.history:
    st.subheader("المحادثة")
    # Render messages in reverse (latest at bottom)
    for i in range(0, len(st.session_state.history), 2):
        # pair of user + assistant (if available)
        user_msg = st.session_state.history[i]
        st.markdown(f"**أنت:** {user_msg['content']}")
        if i+1 < len(st.session_state.history):
            assistant_msg = st.session_state.history[i+1]
            st.markdown(f"**المساعد:** {assistant_msg['content']}")
        st.markdown("---")

st.write("نصائح: اذكر أبعاد الغرفة إن أمكن، الطابق، نافذة/إضاءة، وميزانيتك التقريبية.")
