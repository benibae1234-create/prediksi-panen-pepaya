import streamlit as st
import database

def show_auth_page():
    # 🌿 CSS Tema Pepaya
    st.markdown("""
        <style>
        .stApp {
            
        }

        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #2d3436;
        }

        .subtitle {
            text-align: center;
            font-size: 16px;
            color: #2d3436;
            margin-bottom: 30px;
        }

        

        /* tombol login */
        div.stButton > button {
            background: linear-gradient(90deg, #ff7e00, #ffb347);
            color: white;
            border-radius: 10px;
            height: 45px;
            font-weight: bold;
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #e56b00, #ffa733);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='title'> Sistem Prediksi Pepaya</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analisis & Prediksi Hasil Panen Lebih Mudah dan Cepat</div>", unsafe_allow_html=True)

    # Layout tengah
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        tab1, tab2, tab3 = st.tabs([
            "🔐 Login",
            "📝 Daftar Akun",
            "🔑 Lupa Password"
        ])

        # LOGIN
        with tab1:
            st.subheader("Selamat Datang")

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Masukkan username atau email")
                password = st.text_input("Password", type="password", placeholder="Masukkan password")

                submit_button = st.form_submit_button("Masuk Sekarang", use_container_width=True)

                if submit_button:
                    user = database.verify_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = user[1]
                        st.session_state.email = user[2]
                        st.session_state.role = user[4]
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")

        # REGISTER
        with tab2:
            st.subheader("Daftar Akun Baru ✍️")
            with st.form("register_form"):
                new_user = st.text_input("Username Baru")
                new_email = st.text_input("Email")
                new_pass = st.text_input("Password Baru", type="password")

                submit_reg = st.form_submit_button("Daftar")

                if submit_reg:

                    if database.check_user_exists(new_user):
                        st.error("Username sudah digunakan!")

                    elif database.check_email_exists(new_email):
                        st.error("Email sudah digunakan!")

                    elif "@" not in new_email:
                        st.error("Format email tidak valid!")

                    else:
                        database.register_user(
                            new_user,
                            new_email,
                            new_pass,
                            "user"
                        )

                        st.success("Akun berhasil dibuat! Silakan login.")

            #Lupa Pasword
            with tab3:

                st.subheader("🔑 Reset Password")

                with st.form("forgot_form"):

                    email_reset = st.text_input("Masukkan Email")

                    new_password = st.text_input(
                        "Password Baru",
                        type="password"
                    )

                    submit_reset = st.form_submit_button(
                        "Reset Password"
                    )

                    if submit_reset:

                        if not database.check_email_exists(email_reset):
                            st.error("Email tidak ditemukan!")

                        else:
                            database.reset_password(
                                email_reset,
                                new_password
                            )

                            st.success(
                                "Password berhasil diubah!"
                            )

        st.markdown("</div>", unsafe_allow_html=True)


def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
