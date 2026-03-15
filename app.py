import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="T.C. Akıllı Sağlık Asistanı", page_icon="🇹🇷", layout="centered")

# 2. API Anahtarını Güvenli Şekilde Bağlama
# Not: Streamlit Secrets kısmına GOOGLE_API_KEY olarak eklediğinden emin ol!
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    # En güncel ve stabil model: gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.0-flash')
except Exception as e:
    st.error("Sistem bağlantısında bir sorun var. Lütfen API anahtarını Secrets kısmına eklediğinizden emin olun.")

# 3. Yan Panel (Sidebar) Tasarımı
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>TR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>T.C. Sağlık Teknolojileri</h3>", unsafe_allow_html=True)
    st.write("---")
    st.header("Nasıl Çalışır?")
    st.write("Şikayetinizi yazın, yapay zeka sizi en uygun polikliniğe yönlendirsin.")
    st.warning("ÖNEMLİ: Bu sistem sadece ön bilgilendirme amaçlıdır. Teşhis içermez.")

# 4. Ana Ekran Başlıkları
st.title("🩺 Akıllı Hasta Yönlendirme Asistanı")
st.info("Lütfen şikayetinizi detaylı bir şekilde aşağıya yazınız.")

# 5. Kullanıcı Girişi
sikayet = st.text_area("Şikayetiniz:", placeholder="Örn: Midemde yanma var ve başım dönüyor...")
gonder_butonu = st.button("Şikayetimi Analiz Et")

# 6. Analiz Süreci
if gonder_butonu and sikayet:
    try:
        with st.spinner('Yapay zeka analiz ediyor, lütfen bekleyin...'):
            prompt = f"""
            Sen profesyonel bir sağlık yönlendirme asistanısın. 
            Kullanıcının şu şikayetini analiz et: '{sikayet}'
            Bu şikayete göre hangi polikliniğe (bölüme) gitmesi gerektiğini söyle. 
            Cevabını kısa, net ve güven verici bir dille ver. 
            En sonda mutlaka 'Bu bir tıbbi tavsiye değildir, acil durumlarda 112'yi arayın' uyarısını yap.
            """
            response = model.generate_content(prompt)
            
            st.markdown("---")
            st.subheader("Asistanın Değerlendirmesi:")
            st.success(response.text)
            
    except Exception as e:
        st.error(f"Bir hata oluştu: API anahtarınızı veya internet bağlantınızı kontrol edin.")
elif gonder_butonu and not sikayet:
    st.warning("Lütfen önce şikayetinizi yazın.")

# Sayfa Sonu Alt Bilgi
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: gray;'>Bu proje Karamanlı Mehmetbey Üniversitesi öğrencisi tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
