from database import *

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
        
    DSN = "postgresql://postgres:Home7527647@localhost:5432/products_db"
    engine = sq.create_engine(DSN)
    # create_tables(engine)
    # delete_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # db_filling(session)
    # create_shopping_list(session)
    # clear_shopping_list(session)
    # def add_product(ses):
    # add_product_full(session)
    # category_list(session)
    # product_list(session)
    # shopping_list_week_view(session)
    # check_products(session)
    # shopping_list_view(session)
