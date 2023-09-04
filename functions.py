from database import *

from random import randint
from datetime import date

from sqlalchemy import desc

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)

def categories_list(ses): #список всех категорий
    print('Доступны следующие категории:')
    for cat in ses.query(Category).all():
        print(cat)

def products_list(ses): # список всех продуктов по категориям
    print('Товары:')
    for prod in ses.query(Category).join(Product.category).all():
        print(f'Категория {prod.name}:')
        for pr in prod.products:
            print(f'- {pr} id:{pr.id}') 
            
def shops_list(ses): # список всех магазинов
    print('Магазины:') 
    for shop in ses.query(Shop).all():
        # print(shop)
        print(f'{shop.id}: {shop.name} по адресу {shop.adress}')

def shop_products_list(ses):     # товары, которые можно купить в магазине
    shops_list(ses)
    shop = input('Введите id магазина: ')
    print('Товары, которые можно купить в магазине: ')
    subq = ses.query(Shop).filter(Shop.id==shop).subquery("0")
    subq1 = ses.query(Product_Shop).join(subq, Product_Shop.shop_id==subq.c.id).subquery("1")
    q = ses.query(Product).join(subq1, Product.id == subq1.c.product_id)
    for pr in q:
        print(pr.name)
    return shop

def product_shops_list(ses): #магазины, в которых можно купить выбранный товар
    products_list(ses)
    product = input('Введите id продукта: ')
    print('Магазины, где можно купить товар:')
    subq = ses.query(Product).filter(Product.id==product).subquery("0")
    subq1 = ses.query(Product_Shop).join(subq, Product_Shop.product_id==subq.c.id).subquery("1")
    q = ses.query(Shop).join(subq1, Shop.id==subq1.c.shop_id)
    for shop in q:
        print(f'{shop.name} по адресу {shop.adress}')
    return product

def templates_list(ses):
    print('Шаблоны для списка покупок:')
    for temp in ses.query(Sl_template).all():
        print(temp)

def template_list(ses): # вывести шаблон для покупок, мб выводить только не архивные шаблоны
    templates_list(ses)
    template = input('Введите id шаблона: ')
    subq = ses.query(Sl_template).filter(Sl_template.id==template).subquery("0")
    subq1 = ses.query(Sl_template_pruduct).join(subq, Sl_template_pruduct.sl_template_id==subq.c.id).subquery("1")
    q = ses.query(Product).join(subq1, Product.id==subq1.c.product_id)
    for prod in q:
        print(prod.name)
    print('!!! Добавить вывод количества')
    return template

def add_category(ses): # добавить новую категорию
    name = input('Введите наименование новой категории: ')
    new_category = Category(name=name)
    ses.add(new_category)
    ses.commit()
    print(f'Добавлена категория {name}')
    return new_category

def add_shop(ses): # добавить новый магазин
    name = input('Введите название магазина: ')
    adress = input('Введите адрес магазина (необязательный параметр): ')
    comment = input('Введите комментарий (необязательный параметр): ')
    new_shop = Shop(name=name, adress=adress, comment=comment)
    ses.add(new_shop)
    ses.commit()
    print(f'Добавлен магазин {name} по адресу {adress} ({comment})')
    return new_shop

def add_product_(ses): # добавить новый продукт (без добавления в магазин)
    name = input('Введите наименование товара: ')
    unit = input('Введите едиицы измерения товара: ')
    categories_list(ses)
    category_id = input(
        '''Введите id категории, к которой относится товар. 
    Если подходящей категории нет в списке, введите "0" 
    для создания новой категории: ''')
    if category_id == '0':
        new_category = add_category(ses)
        category_id = new_category.id
    new_product = Product(name=name, unit=unit, category_id=category_id)
    ses.add(new_product)
    ses.commit()    
    # product_id = new_product.id
    print(f'В категорию {category_id} добавлен {name}') # для вывода наименования категории нужен доп запрос
    return new_product


def add_shops_for_product(ses,product_id):
    answer = 'y'
    while answer == 'y':
        shops_list(ses)
        shop_id = input('''Введите id магазина, в котором продается товар. 
                        Если подходящего магазина нет в списке, введите "0"
                        для создания нового магазина: ''')
        if shop_id=='0':
            new_shop = add_shop(ses)
            shop_id = new_shop.id
        price = input('Введите цену товара в магазине (необязательный параметр): ')
        ses.add(Product_Shop(product_id=product_id,shop_id=shop_id,price=price))
        print(f'Товар {product_id} добавлен в магазин {shop_id}') # для вывода наименования магазина нужен доп запрос 
        answer = input('Хотите добавить еще магазин? (y/n)')
    ses.commit()

def add_products_for_shop(ses,shop_id):
    answer = 'y'
    while answer == 'y':
        products_list(ses)
        product_id = input('''Введите id товара, который продается в магазине. 
                        Если подходящего товара нет в списке, введите "0"
                        для создания нового товара: ''')
        if product_id=='0':
            new_product = add_product_(ses)
            product_id = new_product.id
        price = input('Введите цену товара в магазине (необязательный параметр): ')
        ses.add(Product_Shop(product_id=product_id,shop_id=shop_id,price=price))
        print(f'Товар {product_id} добавлен в магазин {shop_id}') # для вывода наименования магазина нужен доп запрос 
        answer = input('Хотите добавить еще магазин? (y/n)')
    ses.commit()

def add_product_shop(ses):
    choice = input('Добавить магазины к товару - введите "1", добавить товары в магазин - введите "2": ')
    if choice == '1':
        # products_list(ses)
        # product_id = input('Введите id продукта, для которого нужно добавить инормацию о наличии в магазинах: ')
        product_id = product_shops_list(ses)
        add_shops_for_product(ses,product_id)
    elif choice == '2':
        shop_id = shop_products_list(ses)
        # shops_list(ses)
        # shop_id = input('Введите id магазина в который хотите добавить продукты: ')
        add_products_for_shop(ses,shop_id)
    else:
        print('Неверный ввод')

def add_product(ses):
    new_product = add_product_(ses)
    product_id = new_product.id
    name = new_product.name
    answer = input(f'Хотите довавить магазины, в которых можно купить {name}? (y/n)' )
    if answer == 'y':
        while answer == 'y':
            shops_list(ses)
            shop_id = input('''Введите id магазина, в котором продается товар. 
                            Если подходящего магазина нет в списке, введите "0"
                            для создания нового магазина: ''')
            if shop_id=='0':
                new_shop = add_shop(ses)
                shop_id = new_shop.id
            price = input('Введите цену товара в магазине (необязательный параметр): ')
            ses.add(Product_Shop(product_id=product_id,shop_id=shop_id,price=price))
            print(f'Товар {name} добавлен в магазин {shop_id}') # для вывода наименования магазина нужен доп запрос 
            answer = input('Хотите добавить еще магазин? (y/n)')
        ses.commit()    
        print(f'Информация о наличии {name} в магазинах внесена')

def add_product_in_template(ses,template_id):
    products_list(ses)
    product_id = input('Введите id продукта для добавление в список: ')
    amount = input('Введите количество товара: ')
    ses.add(Sl_template_pruduct(sl_template_id=template_id, product_id=product_id, amount=amount))
    print(f'!Предварительно! Добавлен товар {product_id} в {template_id}')

def add_products_in_template(ses):
    template_id = template_list(ses)
    answer = 'y'
    while answer == 'y':
        add_product_in_template(ses,template_id)
        answer = input('Хотите добавить еще товар?(y/n) ')
    ses.commit()
    print('Товары добавлены в шаблон')

def create_sl_template(ses):
    name = input('Введите название шаблона: ')
    comment =input('Введите комментарий (необязательный параметр): ')
    new_template = Sl_template(name=name,comment=comment,archive=False)
    ses.add(new_template)
    ses.commit()
    print(f'Создан шаблон {name}')
    answer = input('Хотите добавить товары в шаблон?(y/n) ')
    while answer == 'y':
        add_product_in_template(ses,new_template.id)
        answer = input('Хотите добавить еще товар?(y/n) ')
    ses.commit()
    print('Товары добавлены в шаблон')
    # return new_template

def create_shopping_list_(ses):
    date_ = date.today()
    comment = input('Введите комментарий (необязательный параметр): ')
    new_shopping_list = Shopping_list(date=date_,comment=comment)
    ses.add(new_shopping_list)
    ses.commit()
    print('Создан список покупок')
    return new_shopping_list

def add_products_from_template(ses,shopping_list_id):
    answer = 'y'
    while answer == 'y':
        templates_list(ses)
        template = input('Введите id шаблона: ')
        q = ses.query(Sl_template_pruduct).filter(Sl_template_pruduct.sl_template_id==template).all()
        for pos in q:
            new_pos_sl_product = Shopping_list_product(
                shopping_list_id = shopping_list_id,
                product_id = pos.product_id,
                amount = pos.amount,
                sl_template_id = template
            )
            ses.add(new_pos_sl_product)
        print(f'!Предварительно! товары из шаблона {template} добавлены в список покупок')
        answer = input('Хотите добавить в список покупок товары из другого шаблона?(y/n)')
    ses.commit()

def add_products_from_common_list(ses,shopping_list_id):
    answer = 'y'
    while answer == 'y':
        products_list(ses)
        product_id = input('Введите id продукта: ')
        amount = input('Введите количество товара: ')
        new_pos = Shopping_list_product(
            shopping_list_id = shopping_list_id,
            product_id = product_id,
            amount = amount
        )
        ses.add(new_pos)
        print(f'!Предварительно! Товар {product_id} добавлен в список покупок')
        answer = input('Хотите добавить в список покупок еще товары?(y/n)')
    ses.commit()

def create_shopping_list(ses):
    new_sl = create_shopping_list_(ses)
    sl_id = new_sl.id
    answer1 = input('Хотите добавить в список покупок товары из шаблона?(y/n)')
    if answer1 == 'y':
        add_products_from_template(ses,sl_id)
    answer2 = input('Хотите добавить в список покупок товары из основного списка?(y/n)')
    if answer2 == 'y':
        add_products_from_common_list(ses,sl_id)

choice_dict = {
    '01': categories_list,
    '02': products_list,
    '03': shops_list,
    '04': shop_products_list,
    '05': product_shops_list,
    '06': templates_list,
    '07': template_list,
    '08': add_category,
    '09': add_shop,
    '10': add_product,
    '11': add_product_shop,
    '12': create_sl_template,
    '13': add_products_in_template,
    '14': create_shopping_list

}

def main_choice(ses):
    while True:
        print('''
        Добро пожаловать!
        Досупны следующие команды (идентификатор для ввода указан в скобках):
        - вывод списка категорий (01)
        - вывод списка всех продуктов (02)
        - вывод списка магазинов (03)
        - вывод списка товаров, доступных в конкретном магазине (04)
        - вывод списка магазанов, в которых доступен конкретный товар (05)
        - вывод списка шаблонов для списка покупок (06)
        - вывод списка товаров конкретного шаблона (07)
        - добавить новую категорию (08)
        - добавить новый магазин (09)
        - добавить новый товар в скипок товаров (10)
        - добавить товар в мвгвзин/магазин к товару (11)
        - создать шаблон (12)
        - добавить товар в существующий шаблон (13)
        - создать список покупок (14)

        Для выхода введите "00"
        ''')
        choice = input('Введите идентификатор команды:')
        if choice == '00':
            break
        choice_dict[choice](ses)
    
# функции для тестового заполнение таблиц
def add_product_shop_pos(ses):
    for i in range(30):
        ses.add(Product_Shop(product_id = randint(3,12),shop_id = randint(1,4), price = randint(0,100)))
    ses.commit()    

def sl_template_product(ses):
    for i in range(30):
        ses.add(Sl_template_pruduct(product_id = randint(3,12),sl_template_id = randint(1,5), amount = randint(1,4)))
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


  

