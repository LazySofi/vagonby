from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, Session
import pandas as pd


engine = create_engine('sqlite:///test.db')
Base = declarative_base()

class Vagon(Base):
    __table__ = Table('vagon', Base.metadata)
    Table('vagon', Base.metadata, autoload_with=engine, extend_existing=True)
    id = __table__.c['index']
    model = __table__.c['Модель']
    model_number = __table__.c['Номер модели']
    name =  __table__.c['Наименование']
    gr_vagon = __table__.c['Группа вагонов']

    def get_column_headers(self, table_name = 'vagon'):
        # Получение объекта таблицы по имени
        table = Table(table_name, Base.metadata, autoload=True)

        # Получение заголовков столбцов
        column_headers = table.columns.keys()
        dr = ['index', 'Модель', 'Номер модели', 'Наименование', 'Наименование', 'Группа вагонов']
        column_headers = [i for i in column_headers if i not in dr]
        column_headers = ['id', 'model', 'model_number', 'name', 'gr_vagon'] + column_headers

        return column_headers
        

if __name__ == "__main__":
    """ with Session(engine) as session:
            a = session.query(Vagon.id, Vagon.model, Vagon.name).all()
            df = pd.DataFrame(a)
    print(df) """
    print(Vagon.get_column_headers())