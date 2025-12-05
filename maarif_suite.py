import streamlit as st
import google.generativeai as genai
from groq import Groq
import tempfile
import os
from io import BytesIO 
from docx import Document 

# --- 1. GÜVENLİK VE API AYARLARI ---

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GOOGLE_API_KEY or not GROQ_API_KEY:
    st.error("HATA: Google API Anahtarı ve/veya Groq API Anahtarı bulunamadı! Lütfen secrets dosyasını kontrol edin.")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Gemini API Hatası: {e}")

try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Groq API Hatası: {e}")

# --- 2. YARDIMCI FONKSİYONLAR ---

def tr_duzelt(metin):
    """Sadece görüntüleme için basit karakter düzeltme."""
    dic = {'ğ':'g', 'Ğ':'G', 'ş':'s', 'Ş':'S', 'ı':'i', 'İ':'I', 'ç':'c', 'Ç':'C', 'ü':'u', 'Ü':'U', 'ö':'o', 'Ö':'O'}
    for k, v in dic.items():
        metin = metin.replace(k, v)
    return metin

# 3. WORD FONKSİYONU (SINAV ASİSTANI İÇİN)
def create_exam_word(sorular_kismi, cevaplar_kismi):
    doc = Document()
    doc.add_heading('SINAV KAĞIDI', 0)
    doc.add_paragraph(sorular_kismi)
    doc.add_page_break()
    doc.add_heading('CEVAP ANAHTARI', 1)
    doc.add_paragraph(cevaplar_kismi)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()

# 4. WORD FONKSİYONU (TOPLANTI ASİSTANI İÇİN)
def create_meeting_word(tutanak_metni, transkript_metni):
    doc = Document()
    doc.add_heading('TOPLANTI TUTANAĞI RAPORU', 0)
    doc.add_heading('1. YAPAY ZEKA ÖZETİ', 1)
    doc.add_paragraph(tutanak_metni)
    doc.add_page_break()
    doc.add_heading('2. ORİJİNAL KONUŞMA DÖKÜMÜ (TRANSKRİPT)', 1)
    doc.add_paragraph(transkript_metni)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()


# 5. CLEAR STATE
def meeting_clear_state():
    st.session_state.meeting_tutanak = None
    st.session_state.meeting_transkript = None


# --- 6. ANA SAYFA VE TABLAR (LOGOSUZ YENİ TASARIM) ---
st.set_page_config(
    page_title="Maarif Suite",
    page_icon="🎓",
    layout="wide" 
)

# LOGO KALDIRILDI, BAŞLIKLAR BÜYÜTÜLDÜ VE ORTALANDI

# Büyük Başlık (H1, font-size: 3.5em)
st.markdown(
    "<h1 style='text-align: center; color: #1E3A8A; font-size: 3.5em;'>MAARİF SUITE</h1>", 
    unsafe_allow_html=True
)

# Alt Başlık (P, font-size: 1.3em)
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 1.3em;'>Eğitim Teknolojilerinde İki Güç Bir Arada</p>", 
    unsafe_allow_html=True
)
st.write("---") 

tab_exam, tab_meeting, tab_about = st.tabs(["🎓 SINAV ASİSTANI (Gemini)", "🎙️ TOPLANTI ASİSTANI (Groq)", "ℹ️ HAKKINDA"])

# ----------------------------------------------------------------------
#                         TAB 3: HAKKINDA
# ----------------------------------------------------------------------

with tab_about:
    st.header("Vizyonumuz ve Hakkımda")
    st.subheader("👨‍💻 Geliştirici: Nejdet TUT
