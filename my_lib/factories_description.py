import streamlit as st
import pandas as pd
import numpy as np
import my_lib.lib_sql as ls

def factories_description(manufacturer='Акционерное общество "Научно-производственная корпорация "Уралвагонзавод" имени Ф.Э. Дзержинского (клеймо 5)'):
    
    st.subheader(manufacturer)
    cols = ls.Vagon.get_column_headers(ls.engine)
    cols.remove('id')
    cols.remove('gr_vagon')

    with ls.Session(ls.engine) as session:
        q = session.query(ls.Vagon.model, ls.Vagon.model_number, ls.Vagon.name).filter(ls.Vagon.__table__.c['Завод-изготовитель'] == manufacturer).all()
        df = pd.DataFrame(q)

    st.write('Производимые вагоны:')
    df['Модель'] = df.apply(lambda x: x['name'] + ' мод. ' + x['model'] if np.isnan(x['model_number']) else x['name'] + ' мод. ' + x['model'] + ' ' + str(int(x['model_number'])), axis=1)
    df.insert(loc=0, column='Характеристики', value=False)
    df_button = st.data_editor(df,hide_index=True, use_container_width=True)

    try:
        model_button = df_button.loc[df_button['Характеристики'], ['model', 'model_number']].values.tolist()
    except:
        model_button = []
    
    return model_button


def factories():
    with ls.Session(ls.engine) as session:
        q = session.query(ls.Vagon.__table__.c['Завод-изготовитель']).all()
        df = pd.DataFrame(q).dropna()
        df['Клеймо'] = df.apply(lambda x: x.str.split("клеймо ").str[-1].str[:-1], axis=1)
        df['Завод-изготовитель'] = df.apply(lambda x: x['Завод-изготовитель'].split("(")[0].strip(), axis=1)
        style = df.style.hide(axis=0)
    st.write(style.to_html(), unsafe_allow_html=True)

if __name__ == "__main__":
    factories_description()




