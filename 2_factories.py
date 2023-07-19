import streamlit as st
import pandas as pd
import numpy as np
import my_lib.lib_sql as ls
from my_lib.wagon_description import wagon_description


st.set_page_config(
    page_title = 'Предприятия',
) 

def make_clickable(link, text, factories):
    st.session_state.factories = factories
    return f'<a target="_self" href="{link}">{text}</a>'

df = pd.read_csv('excel_files/factories.csv')






""" url = 'http://localhost:8501/factories_desc' ####
df['Название пред­прия­тия'] = df.apply(lambda x: make_clickable(url, x['Название пред­прия­тия'], x['Код пред­прия­тия']), axis=1)
df = df.head(15).to_html(escape=False, index=False)
st.write(st.session_state.factories)
st.write(df, unsafe_allow_html=True) """



