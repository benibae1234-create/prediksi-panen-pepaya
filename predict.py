import streamlit as st
import tensorflow as tf
import joblib
import numpy as np
import database
import os
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.layers import Dense

# ==============================
# FIX MODEL LOAD (ANTI ERROR)
# ==============================
class FixedDense(Dense):
    def __init__(self, *args, **kwargs):
        kwargs.pop('quantization_config', None)
        super().__init__(*args, **kwargs)

@st.cache_resource
def load_assets():
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'model', 'model_lstm_panen1.h5')
    scaler_path = os.path.join(base_path, 'model', 'scaler1.save')

    try:
        with CustomObjectScope({'Dense': FixedDense}):
            model = tf.keras.models.load_model(model_path, compile=False)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except:
        return None, None

# ==============================
# MAIN PAGE
# ==============================
def show_predict_page():

    tab_home, tab_app = st.tabs(["🏠 Beranda", "🌱 Analisis Lahan"])

    # ================= BERANDA =================
    with tab_home:
        st.markdown("<h1 class='center-text'>🥭 SIPAYA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='center-text'>Sistem Prediksi Hasil Panen Pepaya</p>", unsafe_allow_html=True)

        with st.container(border=True):
            st.info("""
            Sistem ini membantu petani memprediksi hasil panen pepaya berdasarkan kondisi lahan.
            
            📊 Anda cukup memasukkan data:
            - Curah hujan
            - Luas Lahan
            - Jarak Tanam
            - Jumlah Pohon
            - Jumlah pupuk
            - Umur tanaman
            - Dan Hasil Panen sebelumnya
            
            🎯 Sistem akan memberikan:
            - Estimasi hasil panen
            - Indikator naik/turun
            - Rekomendasi perbaikan
            """)

        st.markdown("### 🌿 Indikator Hasil")
        col1, col2 = st.columns(2)

        col1.success("🟢 Hasil meningkat → kondisi optimal")
        col2.error("🔴 Hasil menurun → perlu perbaikan")


    # ================= ANALISIS =================
    with tab_app:
        st.subheader("🔍 Analisis Kondisi Lahan")

        model, scaler = load_assets()

        if model is None:
            st.error("Model tidak ditemukan.")
            return

        # ================= INPUT =================
        st.write("### 📝 Input Data")

        col1, col2 = st.columns(2)

        hujan = col1.number_input("Curah Hujan (mm)", 0.0)
        lahan = col1.number_input("Luas Lahan (m2)", 0.0)
        jarak = col1.number_input("Jarak Tanam (m)", 0.0)

        pohon = col2.number_input("Jumlah Pohon", 0)
        pupuk = col2.number_input("Jumlah Pupuk (Kg)", 0)
        umur = col2.number_input("Umur Tanaman (bulan)", 0)

        hasil_lalu = st.number_input("Hasil Panen Sebelumnya (Kg)", 0)

        # ================= PREDIKSI =================
        if st.button("🚀 Prediksi"):
            if (
                hujan == 0 and
                lahan == 0 and
                jarak == 0 and
                pohon == 0 and
                pupuk == 0 and
                umur == 0 and
                hasil_lalu == 0
            ):
                st.warning("Silakan isi data terlebih dahulu!")
                return

            try:
                # 🔥 INPUT HARUS SESUAI TRAINING
                data = np.array([[
                    hujan,
                    lahan,
                    jarak,
                    pohon,
                    pupuk,
                    umur,
                    hasil_lalu
                ]])

                # 🔄 SCALER (AUTOMATIC)
                data_scaled = scaler.transform(data)

                # 🔁 FORMAT LSTM
                data_lstm = data_scaled.reshape((1, 1, data_scaled.shape[1]))

                # 🤖 PREDIKSI
                pred = model.predict(data_lstm)
                hasil = round(pred[0][0])
                selisih = hasil - hasil_lalu

                # ================= OUTPUT =================
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)

                    st.subheader("📊 Hasil Prediksi")

                    st.metric(
                        "Estimasi Panen",
                        f"{round(hasil)} Kg",
                        f"{round(selisih)} Kg"
                    )

                    if selisih < 0:
                        st.error("🔴 Hasil Menurun")
                        with st.expander("💡 Rekomendasi"):
                            if pupuk < 10:
                                st.warning("Tambahkan pupuk untuk meningkatkan nutrisi tanaman")
                            if hujan > 250:
                                st.warning("Perbaiki drainase agar tidak terjadi busuk akar")
                    else:
                        st.success("🟢 Hasil Meningkat")
                        st.write("Kondisi lahan sudah optimal, lanjutkan perawatan")

                    st.markdown("</div>", unsafe_allow_html=True)

                # ================= SIMPAN =================
                database.simpan_hasil(
                    st.session_state.username,
                    hujan,
                    lahan,
                    jarak,
                    pohon,
                    pupuk,
                    umur,
                    hasil
                )

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

                
               
