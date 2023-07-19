import streamlit as st
import pandas as pd
import numpy as np
import my_lib.lib_sql as ls
from my_lib.wagon_description import wagon_description


st.set_page_config(
    page_title = 'Грузовые вагоны',
)    

tab1, tab2, tab3 = st.tabs(['Поиск', 'Списки вагонов', 'Характристики'])

# Поиск
col1, col2 = tab1.columns(2)
with col1:
    model = st.text_input('Введите код модели', placeholder='Например: 11-5225')
with col2:
    model_number = st.text_input('Введите номер модели', placeholder='Например: 2016')

if model != '' or model_number !='':
    try:
        with ls.Session(ls.engine) as session:
            q = session.query(ls.Vagon.model, ls.Vagon.model_number, ls.Vagon.name, ls.Vagon.__table__.c['Тележка'], 
                                ls.Vagon.__table__.c['Грузоподъёмность'], ls.Vagon.__table__.c['Объём'],
                                ls.Vagon.__table__.c['Год начала серийного производства'], ls.Vagon.__table__.c['Год окончания серийного производства'],
                                )
            if model != '' and model_number !='':
                q = q.filter(ls.Vagon.model == model, ls.Vagon.model_number==model_number)
            elif model == '' and model_number !='':
                q = q.filter(ls.Vagon.model_number==model_number)
            elif model != '' and model_number =='':
                q = q.filter(ls.Vagon.model == model)

            q = q.order_by(ls.Vagon.model, ls.Vagon.model_number).all()
            df = pd.DataFrame(q)

        df['name'] = df.apply(lambda x: x['name'] + ' мод. ' + x['model'] + ' ' + str(int(x['model_number'])), axis=1)
        df = df.rename(columns={'name': 'Модель'}).drop(columns=['model', 'model_number'])
        df['Грузоподъёмность'] = df.apply(lambda x: None if pd.isnull(x['Грузоподъёмность']) else float(x['Грузоподъёмность'].split()[0]), axis=1)
        df['Объём'] = df.apply(lambda x: None if pd.isnull(x['Объём']) else float(x['Объём'].split()[0]), axis=1)
    
        tab1.dataframe(df, use_container_width=True, hide_index=True,
                column_config = {
                    'Год начала серийного производства': st.column_config.NumberColumn(label='Начало выпуска', format='%d', width='medium'),
                    'Год окончания серийного производства': st.column_config.NumberColumn(label='Окончание выпуска', format='%d', width='medium'),
                    'Грузоподъёмность': st.column_config.NumberColumn(label='Грузоподъёмность, т', format='%.1f'),
                    'Объём': st.column_config.NumberColumn(label='Объём, м^3', format='%.1f'),
                }
                )
    except:
        tab1.write('**Вагоны не найдены**')
tab1.caption('Поиск работает только по полному заголовку (можно добавить частичный)')
tab1.caption('Можно добавить фильтры на грузоподьемность, объем и года')


# Списки вагонов
sheets = ['Полувагоны','Крытые вагоны', 'Вагоны-платформы',
          'Вагоны-цистерны', 'Изотермические вагоны', 'Прочие вагоны']
Sheets = tab2.selectbox("Выберите категорию поиска", sheets)
with ls.Session(ls.engine) as session:
    a = session.query(ls.Vagon.model, ls.Vagon.model_number, ls.Vagon.name, ls.Vagon.__table__.c['Тележка'], 
                            ls.Vagon.__table__.c['Грузоподъёмность'], ls.Vagon.__table__.c['Объём'],
                            ls.Vagon.__table__.c['Год начала серийного производства'], ls.Vagon.__table__.c['Год окончания серийного производства'],
                            ).\
        filter(ls.Vagon.gr_vagon == Sheets).all()
    df = pd.DataFrame(a)
    df['name'] = df.apply(lambda x: x['name'] + ' мод. ' + x['model'] if np.isnan(x['model_number']) else x['name'] + ' мод. ' + x['model'] + ' ' + str(int(x['model_number'])), axis=1)
    df = df.rename(columns={'name': 'Модель'}).drop(columns=['model', 'model_number'])
    df['Грузоподъёмность'] = df.apply(lambda x: None if pd.isnull(x['Грузоподъёмность']) else float(x['Грузоподъёмность'].split()[0]), axis=1)
    df['Объём'] = df.apply(lambda x: None if pd.isnull(x['Объём']) else float(x['Объём'].split()[0]), axis=1)

    
tab2.dataframe(df, use_container_width=True, hide_index=True,
               column_config = {
                    'Год начала серийного производства': st.column_config.NumberColumn(label='Начало выпуска', format='%d', width='medium'),
                    'Год окончания серийного производства': st.column_config.NumberColumn(label='Окончание выпуска', format='%d', width='medium'),
                    'Грузоподъёмность': st.column_config.NumberColumn(label='Грузоподъёмность, т', format='%.1f'),
                    'Объём': st.column_config.NumberColumn(label='Объём, м^3', format='%.1f'),
               }
               )

tab2.caption('Можно добавить фильтры на грузоподьемность, объем и года')

# Характристики

with tab3:
    wagon_description()

