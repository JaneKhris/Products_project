from database import *
from functions import *

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
        
    DSN = "postgresql://postgres:Home7527647@localhost:5432/products_db"
    engine = sq.create_engine(DSN)
    # create_tables(engine)
    # delete_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # categories_list(session)
    # products_list(session)
    # shops_list(session)
    # add_product_shop_pos(session)
    # shop_products_list(session)

    # sl_template_product(session)
    # shopping_list_product(session)
    # purchased_product(session)