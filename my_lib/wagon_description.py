import streamlit as st
import pandas as pd
import my_lib.lib_sql as ls

def wagon_description(model = '11-5225', model_number = '2016'):

    st.header(f'Модель {model} {model_number}')
    st.subheader('Технические характеристики вагона')
    cols = ls.Vagon.get_column_headers(ls.engine)
    cols.remove('id')
    cols.remove('gr_vagon')

    wagon = dict()
    with ls.Session(ls.engine) as session:
        q = session.query(ls.Vagon).filter(ls.Vagon.model == model, ls.Vagon.model_number==model_number).first()
        for col in cols:
            attr = getattr(q, col)
            if not pd.isnull(attr):
                wagon[col]=[attr]
    df = pd.DataFrame.from_dict(wagon).rename(columns={'model': 'Модель', 'model_number': 'Номер модели', 'name': 'Наименование'})
    for i in ['Номер модели', 'Год начала серийного производства', 'Год окончания серийного производства']:
        if i in df.columns and df[i].dtypes == float:
            df[i] = df[i].astype(int)
    df = df.T.rename(columns ={0: 'feature'})
    df.reset_index(inplace=True)
    df['feature'] = df['feature'].astype(str)

    style = df.style.hide(axis=0)
    style.hide(axis=1)
    st.write(style.to_html(), unsafe_allow_html=True)

def color_rows(r):
    return ['background-color: white']*len(r) if r.duplicated().sum() == 0 else ['background-color: rgba(255, 255, 128, .3)']*len(r)

    


def wagon_description_all(models = []):

    st.subheader('Технические характеристики вагона')
    cols = ls.Vagon.get_column_headers(ls.engine)
    cols.remove('id')
    cols.remove('gr_vagon')

    wagon = dict()
    dfs = []
    for m in models:
        model = m[0]
        model_number = m[1]

        with ls.Session(ls.engine) as session:
            q = session.query(ls.Vagon).filter(ls.Vagon.model == model, ls.Vagon.model_number==model_number).first()
            for col in cols:
                attr = getattr(q, col)
                wagon[col]=[attr]
        df = pd.DataFrame.from_dict(wagon).rename(columns={'model': 'Модель', 'model_number': 'Номер модели', 'name': 'Наименование'})
        for i in ['Номер модели', 'Год начала серийного производства', 'Год окончания серийного производства']:
            if i in df.columns and df[i].dtypes == float:
                df[i] = df[i].astype(int)

        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    ids = len(df)
    cols = df.columns
    for col in cols:
        if df[col].isna().sum()==ids:
            df = df.drop([col], axis=1)
    df = df.T
    df.reset_index(inplace=True)
    style = df.style.apply(color_rows, axis=1).hide(axis=0)
    style.hide(axis=1)
    st.write(style.to_html(), unsafe_allow_html=True, )

    

if __name__ == "__main__":
    wagon_description(model = '11-5225', model_number = '2016')