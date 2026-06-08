import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import time

def show_admin_page():
    file_path = 'data_panen.csv'

    # ================= SIDEBAR =================
    with st.sidebar:
        st.markdown("""
        <style>
        .profile-name {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: -5px;
        }
        .profile-role {
            font-size: 12px;
            color: gray;
            margin-top: 0px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1,3])

        with col1:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=50
            )

        with col2:
            st.markdown(
                "<div class='profile-name'>Admin</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div class='profile-role'>Administrator Sistem</div>",
                unsafe_allow_html=True
            )

        st.divider()

        menu = st.radio(
            "📂 Menu",
            ["📊 Dashboard", "📁 Data Panen"]
        )

    # ================= DASHBOARD =================
    if menu == "📊 Dashboard":
        st.title("📊 Dashboard Admin")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.index = df.index + 1

            # ================= METRIC =================
            col1, col2, col3 = st.columns(3)

            col1.metric("Total Data", len(df))
            col2.metric("User Aktif", df['User'].nunique())
            col3.metric(
                "Rata-rata Hasil (Kg)",
                round(df['Hasil_Prediksi'].mean(), 2)
            )

            # ================= GRAFIK UTAMA =================
            st.write("### 📈 Grafik Tren Prediksi Hasil Panen")

            fig, ax = plt.subplots(figsize=(10,5))

            ax.plot(
                df.index,
                df['Hasil_Prediksi'],
                marker='o'
            )

            ax.set_xlabel("Data Ke-")
            ax.set_ylabel("Hasil Prediksi Panen (Kg)")
            ax.set_title("Grafik Hasil Prediksi Panen Pepaya")
            ax.grid(True)

            st.pyplot(fig)

                           # ================= DATA PANEN =================
    elif menu == "📁 Data Panen":
        st.title("📁 Manajemen Data Panen")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.index = df.index + 1

            # ================= SEARCH =================
            st.write("### 🔍 Cari Data Berdasarkan Username")

            search = st.text_input("Masukkan Username")

            if search:
                filtered_df = df[
                    df['User'].str.contains(search, case=False)
                ]
                st.dataframe(
                    filtered_df,
                    use_container_width=True
                )
            else:
                st.write("### 🔍 Data Prediksi Petani")
                st.dataframe(
                    df,
                    use_container_width=True
                )

            # ================= BUTTON =================
            col1, col2 = st.columns(2)

            # Hapus semua data
            with col1:
                if st.button("🗑️ Hapus Semua Data"):
                    os.remove(file_path)
                    st.success(
                        "Semua data berhasil dihapus!"
                    )
                    st.rerun()

            # Download data
            with col2:
                st.download_button(
                    label="⬇️ Download CSV",
                    data=df.to_csv(index=False),
                    file_name="data_panen.csv",
                    mime="text/csv"
                )

            st.divider()

            # ================= HAPUS PER BARIS =================
            st.write("### ❌ Hapus Data Tertentu")

            selected_index = st.number_input(
                "Masukkan Index Data",
                min_value=1,
                max_value=len(df),
                step=1
            )

            if st.button("Hapus Data Ini"):

                # Simpan nomor yang dihapus
                deleted_data = selected_index

                # Hapus data
                df = df.drop(selected_index)

                # Reset index
                df = df.reset_index(drop=True)

                # Mulai index dari 1 lagi
                df.index = df.index + 1

                # Simpan
                df.to_csv(
                    file_path,
                    index=False
                )

                # Notifikasi berhasil
                st.success(
                    f"✅ Data ke-{deleted_data} berhasil dihapus!"
                )

                # Delay agar notif terlihat
                time.sleep(5)

                st.rerun()

        else:
            st.info("Belum ada data masuk.")

# ================= FUNGSI SIMPAN =================
def simpan_hasil(
    username,
    hujan,
    lahan,
    jarak,
    pohon,
    pupuk,
    umur,
    hasil
):
    file_path = 'data_panen.csv'

    data = {
        'Tanggal': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'User': username,
        'Hujan': hujan,
        'Luas_Lahan': lahan,
        'Jarak_Tanam': jarak,
        'Jumlah_Pohon': pohon,
        'Pupuk': pupuk,
        'Umur': umur,
        'Hasil_Prediksi': hasil
    }

    df = pd.DataFrame([data])

    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(
            file_path,
            mode='a',
            header=False,
            index=False
        )

# ================= LOGIN =================
def verify_user(u, p):
    file_path = 'users.csv'

    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)

    user = df[
        (
            (df['username'] == u) |
            (df['email'] == u)
        ) &
        (df['password'] == p)
    ]

    if not user.empty:
        row = user.iloc[0]

        return (
            row['id'],
            row['username'],
            row['email'],
            row['password'],
            row['role']
        )

    return None
# ================= CHECK USER =================
def check_user_exists(u):
    file_path = 'users.csv'

    if not os.path.exists(file_path):
        return False

    df = pd.read_csv(file_path)

    return u in df['username'].values

def check_email_exists(e):
    file_path = 'users.csv'

    if not os.path.exists(file_path):
        return False

    df = pd.read_csv(file_path)

    return e in df['email'].values

# ================= REGISTER =================
def register_user(u, e, p, r="user"):
    file_path = 'users.csv'

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        new_id = df['id'].max() + 1
    else:
        df = pd.DataFrame(
            columns=[
                'id',
                'username',
                'email',
                'password',
                'role'
            ]
        )
        new_id = 1

    new_user = pd.DataFrame([{
        'id': new_id,
        'username': u,
        'email' : e,
        'password': p,
        'role': r
    }])

    df = pd.concat(
        [df, new_user],
        ignore_index=True
    )

    df.to_csv(file_path, index=False)

    return True

# ================= RESET PASSWORD =================
def reset_password(email, new_password):

    file_path = 'users.csv'

    if not os.path.exists(file_path):
        return False

    df = pd.read_csv(file_path)

    df.loc[
        df['email'] == email,
        'password'
    ] = new_password

    df.to_csv(file_path, index=False)

    return True
