# thai_dictionary_web.py
import streamlit as st
import wikipedia
import json
from fuzzywuzzy import process
from gtts import gTTS
import base64
import os

wikipedia.set_lang("th")

MEMORY_FILE = "thai_dict_memory.json"
try:
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
except:
    memory = {}

# ===== ฟังก์ชันบันทึกคลังความจำ =====
def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ===== สร้างเสียงจากข้อความ =====
def create_audio(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='th')
    tts.save(filename)
    with open(filename, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# ===== ค้นหาคำศัพท์ =====
def search_word(word):
    if word in memory:
        return f"📚 จากคลังความรู้:\n\n{memory[word]}", memory[word]
    try:
        summary = wikipedia.summary(word, sentences=2)
        return f"🌐 จาก Wikipedia:\n\n{summary}", summary
    except:
        close_match, score = process.extractOne(word, memory.keys())
        if score > 80:
            return f"🔍 ใกล้เคียง: '{close_match}'\n\n{memory[close_match]}", memory[close_match]
        return "❌ ไม่พบข้อมูลคำนี้ และไม่มีคำใกล้เคียง", None

# ===== UI สไตล์เฟี้ยวๆ =====
st.set_page_config(page_title="📘 พจนานุกรม AI", page_icon="📘", layout="centered")
st.title("📘 พจนานุกรม AI ภาษาไทย (V2 เฟี้ยวๆ)")
st.markdown("---")

query = st.text_input("🔎 คำศัพท์ที่ต้องการค้นหา:")

if query:
    st.markdown("------")
    result, definition = search_word(query.strip())
    st.markdown(f"### 📖 คำอธิบาย\n{result}")

    if definition:
        st.markdown("---")
        st.markdown("🎧 ฟังคำอธิบาย")
        audio_html = create_audio(definition)
        st.markdown(audio_html, unsafe_allow_html=True)

    if "ไม่พบข้อมูล" in result:
        new_def = st.text_area("📝 ช่วยป้อนคำอธิบายใหม่ให้ฉันเรียนรู้:")
        if st.button("💾 บันทึกคำอธิบาย"):
            memory[query.strip()] = new_def.strip()
            save_memory()
            st.success("✅ บันทึกเรียบร้อยแล้ว!")

if st.button("🧹 ล้างหน่วยความจำทั้งหมด"):
    memory = {}
    save_memory()
    st.warning("🔥 ลบข้อมูลทั้งหมดเรียบร้อยแล้ว!")

st.markdown("---")
st.markdown("👤 พัฒนาโดย: Guzz | 💡  ผู้ช่วยโดย ChatGPT")