import streamlit as st
import auth, database, predict

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth.show_auth_page()
else:
    st.sidebar.title(f"Halo, {st.session_state.username}")
    if st.session_state.role == "admin":
        database.show_admin_page()
    else:
        predict.show_predict_page()
    if st.sidebar.button("Logout"): auth.logout()