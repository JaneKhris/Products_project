from database import *
from random import randint

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)

def categories_list(ses):
    print('Доступны следующие категории:')
    for cat in ses.query(Category).all():
        print(cat)

def products_list(ses):
    print('Товары:')
    for prod in ses.query(Category).join(Product.category).all():
        print(f'Категория {prod.name}:')
        for pr in prod.products:
            print(f'- {pr}') 
            
def shops_list(ses):
    print('Магазины:') 
    for shop in ses.query(Shop).all():
        # print(shop)
        print(f'{shop.id}: {shop.name} по адресу {shop.adress}')

def shop_products_list(ses):     #позатать товары которые можно купить в магазине
    shops_list(ses)
    shop = input('Введите id магазина: ')
    subq = ses.query(Shop).filter(Shop.id==shop).subquery("0")
    subq1 = ses.query(Product_Shop).join(subq, Product_Shop.shop_id==subq.c.id).subquery("1")
    q = ses.query(Product).join(subq1, Product.id == subq1.c.product_id)
    for pr in q:
        print(pr.name)

def product_shops_list(ses):
    products_list(ses)
    product = input('Введите id продукта: ')
    subq = ses.query(Product).filter(Product.id==product).subquery("0")
    subq1 = ses.query(Product_Shop).join(subq, Product_Shop.product_id==subq.c.id).subquery("1")
    q = ses.query(Shop).join(subq1, Shop.id==subq1.c.shop_id)
    for shop in q:
        print(f'{shop.name} по адресу {shop.adress}')

def template_list(ses):
    print('Шаблоны для списка покупок:')
    for temp in ses.query(Sl_template).all():
        print(f'{temp.id}: {temp.name}')
    template = input('Введите id шаблона: ')
    subq = ses.query(Sl_template).filter(Sl_template.id==template).subquery("0")
    subq1 = ses.query(Sl_template_pruduct).join(subq, Sl_template_pruduct.sl_template_id==subq.c.id).subquery("1")
    q = ses.query(Product).join(subq1, Product.id==subq1.c.product_id)
    for prod in q:
        print(prod.name)
    print('!!! Добавить вывод количества')


# Заполнение таблиц
def add_product_shop_pos(ses):
    for i in range(30):

        ses.add(Product_Shop(product_id = randint(1,28),shop_id = randint(1,5), price = randint(0,100)))
    ses.commit()    



def sl_template_product(ses):
    for i in range(30):
        ses.add(Sl_template_pruduct(product_id = randint(1,28),sl_template_id = randint(1,5), amount = randint(1,5)))
    ses.commit()  

def shopping_list_product(ses):
    for i in range(30):
        ses.add(Shopping_list_product(product_id = randint(1,28),shopping_list_id = randint(1,5), amount = randint(1,5)))
    ses.commit()  

def purchased_product(ses):
    for i in range(30):
        ses.add(Purchased_product(product_id = randint(1,28), 
                                  amount = randint(1,5),
                                  date = date(2023,8,randint(1,7)),
                                  shop_id = randint(1,5)))
    ses.commit()  


  

