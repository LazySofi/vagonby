import streamlit as st
import pandas as pd
import numpy as np
import my_lib.lib_sql as ls
from my_lib.wagon_description import wagon_description_all
from my_lib.factories_description import factories_description


st.set_page_config(
    page_title = 'Грузовые вагоны',
)   

def drop_list_duplicates(k):
    new_k = []
    for elem in k:
        if elem not in new_k:
            new_k.append(elem)
    return new_k

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Поиск вагонов', 'Списки вагонов', '**Характеристики**', 'Поиск по предприятиям', 'Список предприятий'])

# Поиск
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        model = st.text_input('Введите код модели', placeholder='Например: 11-5225')
    with col2:
        model_number = st.text_input('Введите номер модели', placeholder='Например: 2016')
    col3, col4 = st.columns([3, 1])
    with col3:
        carrying = st.slider(
            'Выберите границы грузоподьемности в тоннах',
            0.0, 500.0, (0.0, 500.0))
    with col4:
        carrying_null = st.checkbox('Включать неизвестную грузоподьемность')


    try:
        with ls.Session(ls.engine) as session:
            q = session.query(ls.Vagon.model, ls.Vagon.model_number, ls.Vagon.name, ls.Vagon.__table__.c['Тележка'], 
                                ls.Vagon.__table__.c['Грузоподъёмность'], ls.Vagon.__table__.c['Объём'],
                                ls.Vagon.__table__.c['Год начала серийного производства'], ls.Vagon.__table__.c['Год окончания серийного производства'],
                                )
            q = q.filter(ls.Vagon.model.like(f'%{model}%'), ls.Vagon.model_number.like(f"%{model_number}%"))
            q = q.order_by(ls.Vagon.model, ls.Vagon.model_number).all()
            df = pd.DataFrame(q)

        df['Модель'] = df.apply(lambda x: x['name'] + ' мод. ' + x['model'] if x['model_number'] is None or np.isnan(x['model_number']) else x['name'] + ' мод. ' + x['model'] + ' ' + str(int(x['model_number'])), axis=1)
        df['Грузоподъёмность'] = df.apply(lambda x: None if pd.isnull(x['Грузоподъёмность']) else float(x['Грузоподъёмность'].split()[0]), axis=1)
        df['Объём'] = df.apply(lambda x: None if pd.isnull(x['Объём']) else float(x['Объём'].split()[0]), axis=1)
        df.insert(loc=0, column='Характеристики', value=False)
        if carrying_null:
            df = df[(df['Грузоподъёмность']>=carrying[0]) & (df['Грузоподъёмность']<=carrying[1]) | df['Грузоподъёмность'].isnull()]
        else:
            df = df[(df['Грузоподъёмность']>=carrying[0]) & (df['Грузоподъёмность']<=carrying[1])]
        
        df_button = st.data_editor(df, use_container_width=True, hide_index=True,
                column_config = {
                    'Год начала серийного производства': st.column_config.NumberColumn(label='Начало выпуска', format='%d', width='medium'),
                    'Год окончания серийного производства': st.column_config.NumberColumn(label='Окончание выпуска', format='%d', width='medium'),
                    'Грузоподъёмность': st.column_config.NumberColumn(label='Грузоподъёмность, т', format='%.1f'),
                    'Объём': st.column_config.NumberColumn(label='Объём, м^3', format='%.1f'),
                },
                disabled=['Модель', 'Тележка','Грузоподъёмность',  'Объём', 'Год начала серийного производства', 'Год окончания серийного производства'],
                column_order=('Характеристики', 'Модель', 'Тележка','Грузоподъёмность',  'Объём', 'Год начала серийного производства', 'Год окончания серийного производства'),
                )
    except:
        st.write('**Вагоны не найдены**')
    st.caption('Поиск работает только по полному и частичному заголовку (%mask%)')
    st.caption('Можно добавить фильтры на грузоподьемность, объем и года')


    try:
        model_button_tab1 = df_button.loc[df_button['Характеристики'], ['model', 'model_number']].values.tolist()
    except:
        model_button_tab1 = []

# Списки вагонов
with tab2:
    sheets = ['Полувагоны','Крытые вагоны', 'Вагоны-платформы',
            'Вагоны-цистерны', 'Изотермические вагоны', 'Прочие вагоны', 'Все',]
    Sheets = st.selectbox("Выберите категорию поиска", sheets)
    with ls.Session(ls.engine) as session:
        a = session.query(ls.Vagon.model, ls.Vagon.model_number, ls.Vagon.name, ls.Vagon.__table__.c['Тележка'], 
                                ls.Vagon.__table__.c['Грузоподъёмность'], ls.Vagon.__table__.c['Объём'],
                                ls.Vagon.__table__.c['Год начала серийного производства'], ls.Vagon.__table__.c['Год окончания серийного производства'],
                                )
        if  Sheets == 'Все':                         
            a = a.all()
        else:
            a = a.filter(ls.Vagon.gr_vagon == Sheets).all()
        df = pd.DataFrame(a)
        df['Модель'] = df.apply(lambda x: x['name'] + ' мод. ' + x['model'] if x['model_number'] is None or np.isnan(x['model_number']) else x['name'] + ' мод. ' + x['model'] + ' ' + str(int(x['model_number'])), axis=1)
        df['Грузоподъёмность'] = df.apply(lambda x: None if pd.isnull(x['Грузоподъёмность']) else float(x['Грузоподъёмность'].split()[0]), axis=1)
        df['Объём'] = df.apply(lambda x: None if pd.isnull(x['Объём']) else float(x['Объём'].split()[0]), axis=1)
        df.insert(loc=0, column='Характеристики', value=False)
        
    tab2_button = st.data_editor(df, use_container_width=True, hide_index=True,
                column_config = {
                        'Год начала серийного производства': st.column_config.NumberColumn(label='Начало выпуска', format='%d', width='medium'),
                        'Год окончания серийного производства': st.column_config.NumberColumn(label='Окончание выпуска', format='%d', width='medium'),
                        'Грузоподъёмность': st.column_config.NumberColumn(label='Грузоподъёмность, т', format='%.1f'),
                        'Объём': st.column_config.NumberColumn(label='Объём, м^3', format='%.1f'),
                },
                    disabled=['Модель', 'Тележка','Грузоподъёмность',  'Объём', 'Год начала серийного производства', 'Год окончания серийного производства'],
                        column_order=('Характеристики', 'Модель', 'Тележка','Грузоподъёмность',  'Объём', 'Год начала серийного производства', 'Год окончания серийного производства'),
                )

    try:
        model_button_tab2 = tab2_button.loc[tab2_button['Характеристики'], ['model', 'model_number']].values.tolist()
    except:
        model_button_tab2 = []

    st.caption('Можно добавить фильтры на грузоподьемность, объем и года')



with tab5:
    with ls.Session(ls.engine) as session:
        q = session.query(ls.Vagon.__table__.c['Завод-изготовитель']).all()
        df_manufacturer = pd.DataFrame(q).dropna().drop_duplicates()
        df_manufacturer['Клеймо'] = df_manufacturer.apply(lambda x: int(x.str.split("клеймо ").str[-1].str[:-1]), axis=1)
        df_manufacturer['Завод-изготовитель'] = df_manufacturer.apply(lambda x: x['Завод-изготовитель'].split("(")[0].strip(), axis=1)
        df_manufacturer = df_manufacturer.sort_values('Клеймо')
    style = df_manufacturer.style.hide(axis=0)
    st.write(style.to_html(), unsafe_allow_html=True)

with tab4:
    manufacturer = st.text_input('Введите клеймо предприятия', placeholder='Например: 5')
    if manufacturer.isnumeric():
        manufacturer_row = df_manufacturer[df_manufacturer['Клеймо'] == int(manufacturer)].iloc[0]
        manufacturer = f'{manufacturer_row["Завод-изготовитель"]} (клеймо {manufacturer})'
        model_button_tab5 = factories_description(manufacturer)
    else:
        model_button_tab5 = []
        st.write('**Введите число**')
        st.caption('Если известно название, а не клеймо, воспользуйтесь поиском по странице (**Ctrl+F**) на вкладке "Список предприятий"')



with tab3:
    try:
        wagon_description_all(drop_list_duplicates(model_button_tab1+model_button_tab2+model_button_tab5))
        
    except:
        st.caption('Выберите вагоны')



