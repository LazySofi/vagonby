import streamlit as st

if 'factories' not in st.session_state:
    st.session_state.factories = 5

st.write(st.session_state.factories)


import pandas as pd

