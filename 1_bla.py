import streamlit as st
from . import bla_bla
from pages import bla_bla_bla

def main():
    st.title("Мультистраничное приложение")
    pages = {
        "Главная": bla_bla,
        "О нас": bla_bla_bla,
    }
    page = st.sidebar.selectbox("Выберите страницу", list(pages.keys()))
    session_state = st.session_state.get('session_state', {'data': None})
    pages[page](session_state)
    st.session_state['session_state'] = session_state

if __name__ == "__main__":
    main()
