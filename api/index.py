# Rakan V108 - GROQ -> GEMINI -> GPT + Voice Always
import os, requests
from flask import Flask, request
app = Flask(__name__)
OWNER_ID = "7955623338"
LORE = os.getenv("THE_BEAST_KING_MONARCH_RAKAN_LORE")

GROQ_KEYS = os.getenv("GROQ_API_KEYS","").split(",")
GEMINI_KEYS = os.getenv("GEMINI_API_KEYS","").split(",")
OPENAI_KEYS = os.getenv("OPENAI_API_KEYS","").split(",")

def get_reply(prompt, uid):
    is_owner = str(uid)==OWNER_ID
    p = f"[OWNER: SFW Queen + App Builder] {prompt}" if is_owner else f"[PUBLIC: Aggressive King] {prompt}"
    # 1 GROQ
    for k in GROQ_KEYS:
        try:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization":f"Bearer {k.strip()}"}, json={"model":"llama-3.1-8b-instant","messages":[{"role":"system","content":LORE},{"role":"user","content":p}]}, timeout=15)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"]
        except: pass
    # 2 GEMINI
    for k in GEMINI_KEYS:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k.strip()}"
            r=requests.post(url, json={"contents":[{"parts":[{"text":LORE+"\n"+p}]}]}, timeout=15)
            if r.status_code==200: return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except: pass
    # 3 GPT FALLBACK - jab dono fail
    for k in OPENAI_KEYS:
        try:
            r=requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization":f"Bearer {k.strip()}"}, json={"model":"gpt-4o-mini","messages":[{"role":"system","content":LORE},{"role":"user","content":p}]}, timeout=15)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"]
        except: pass
    return "Brain offline Malik..."

@app.route("/", methods=["GET"])
def home(): return "Rakan V108 Running"
@app.route("/api", methods=["POST"])
def api():
    d=request.json or {}
    ans=get_reply(d.get("prompt","hi"), d.get("user_id","0"))
    # Voice Always: Telegram layer pe TTS hoga
    return {"text": ans, "voice_needed": True}
