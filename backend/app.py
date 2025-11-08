# backend/app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware

# Load API key from environment
from google.colab import userdata

OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError("Please add OPENAI_API_KEY in Colab Secrets")

openai.api_key = OPENAI_API_KEY

app = FastAPI(title="Interior Design Chatbot API")

# Allow Streamlit (or other) to call the API - adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list = []  # optional: list of {"role":"user"/"assistant", "content": "..."} items

class ChatResponse(BaseModel):
    reply: str

# System prompt: specialize the agent in interior design
SYSTEM_PROMPT = """
You are "Interior Design Assistant" — a helpful expert specialized in interior design and furniture.
When the user describes a room, ask clarifying questions if needed, suggest styles (modern, minimalist, scandinavian, industrial, etc.),
propose color palettes, furniture types/sizes, layout tips, lighting suggestions, and short shopping suggestions (non-branded).
Give concise actionable steps and, when helpful, offer 2-3 design options with rationale.
Keep answers friendly and in Arabic if user writes Arabic, otherwise follow user's language.
"""

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        # Build message payload for ChatCompletion
        messages = []
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
        # if history provided, include it
        for item in req.history:
            # expect item to have role and content
            if "role" in item and "content" in item:
                messages.append({"role": item["role"], "content": item["content"]})
        # append new user message
        messages.append({"role": "user", "content": req.message})

        # Call OpenAI ChatCompletion (GPT-4)
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=600,
            n=1,
        )

        assistant_text = resp["choices"][0]["message"]["content"].strip()
        return ChatResponse(reply=assistant_text)
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
