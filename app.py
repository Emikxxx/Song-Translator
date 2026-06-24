import streamlit as st
from google import genai
from google.genai import types
import re

st.set_page_config(page_title="Tłumacz piosenek koreańskich", page_icon="🎵", layout="centered")

st.title("Tłumacz piosenek koreańskich")
st.write("Wklej tekst piosenki, a AI przetłumaczy ją i wypisze słówka do nauki.")

# BEZPIECZNE POBIERANIE KLUCZA Z USTAWIEŃ STREAMLIT CLOUD
GEMINI_KEY = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=GEMINI_KEY)

SYSTEM_PROMPT = """
Jesteś ekspertem języka koreańskiego.
Odpowiadaj po polsku.
Podaj:
1. Tłumaczenie
2. Słówka do nauki
3. Ciekawostki językowe
"""

def clean_text(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"#+\s*", "", text)
    return text.replace("*", "").strip()

user_input = st.text_area("Wklej tekst piosenki:", height=350)

if st.button("Analizuj"):
    if not user_input.strip():
        st.error("Najpierw wklej tekst piosenki.")
    else:
        with st.spinner("AI analizuje tekst..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2
                )
            )
        st.subheader("Wynik")
        st.write(clean_text(response.text))
