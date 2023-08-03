import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import json
from datetime import date



Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f' {self.id}: {self.name}'
    
class Product(Base):
    __tablename__ = "product"
    id = sq.Column(sq.Integer, primary_key=True)
    name =  sq.Column(sq.String(length=40), unique=True)
    unit = sq.Column(sq.String(length=10))
    category_id = sq.Column(sq.Integer, sq.ForeignKey("category.id"))
    
    category = relationship(Category, backref="products")

    def __str__(self):
        return f'{self.name} ({self.unit})'

class Shopping_list(Base): #текущий список покупок
    __tablename__ = "shopping_list"
    id = sq.Column(sq.Integer, primary_key=True)
    product_id =  sq.Column(sq.Integer, sq.ForeignKey("product.id"))
    amount = sq.Column(sq.Numeric)

    product = relationship(Product, backref="shop_list")

class Shopping_list_week(Base): # стандартный список покупок на неделю
    __tablename__ = "shopping_list_week"
    id = sq.Column(sq.Integer, primary_key=True)
    product_id =  sq.Column(sq.Integer, sq.ForeignKey("product.id"))
    amount = sq.Column(sq.Numeric)

    product = relationship(Product, backref="list_week")


class Purchased_product(Base):
    __tablename__ = "purchased_products"
    id = sq.Column(sq.Integer, primary_key=True)
    product_id =  sq.Column(sq.Integer, sq.ForeignKey("product.id"))
    amount = sq.Column(sq.Numeric)
    date = sq.Column(sq.Date)

    product = relationship(Product, backref="purchased")


def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)


def db_filling(ses): # заполнение базы тестовыми данными

    with open('test_data.json', 'r', encoding="utf-8") as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'category': Category,
            'product': Product,
            'shopping_list_week': Shopping_list_week,
        }[record.get('model')]       
        # ses.add(model(id=record.get('pk'), **record.get('fields')))
        ses.add(model(**record.get('fields')))

    ses.commit()

def category_list(ses):
    print('Доступны следующие категории:')
    for cat in ses.query(Category).all():
        print(cat)

def product_list(ses):
    print('Товары:')
    for prod in ses.query(Category).join(Product.category).all():
        print(f'Категория {prod.name}:')
        for pr in prod.products:
            print(f'- {pr}') 
            

def shopping_list_week_view(ses):
    print('Стандартный список покупок на неделю:')
    for prod in ses.query(Product).join(Shopping_list_week.product).all():
        for pr in prod.list_week:
            print(f'-{prod.name} {pr.amount} {prod.unit}')
        

def shopping_list_view(ses):
    print('Список покупок:')
    for prod in ses.query(Product).join(Shopping_list.product).all():
        for pr in prod.shop_list:
            print(f'-{prod.name} {pr.amount} {prod.unit}')

def purchased_product_list(ses):
    print('Список купленных товаров:')
    for prod in ses.query(Product).join(Purchased_product.product).all():
        for pr in prod.purchased:
            print(f' {prod.name} {pr.amount} {prod.unit} /{pr.date}')

def create_shopping_list(ses): 
    ses.query(Shopping_list).delete()
    q = ses.query(Shopping_list_week)
    for product in q.all():   
        ses.add(Shopping_list(product_id = product.product_id, amount = product.amount))
    label_add = 'y'
    while label_add == 'y':
        label_add = input('Внесены товары, хотите ли добавить еще товар? (y/n)')
        if label_add == 'y':
            add_product_id = input('Введите id товара')
            add_amount = input('Введите количество товара')
            ses.add(Shopping_list(product_id = add_product_id, amount = add_amount))
        elif label_add == 'n':
            print('Спасибо, список покупок сформирован')
            break
        else:
            print('Ошибка, повторите ввод')
            label_add = 'y'
    ses.commit() 

def clear_shopping_list(ses):
    ses.query(Shopping_list).delete()
    ses.commit()

def shopping_list_done(ses): # перенос позиций в купленные товары и очистка списка покупок
    q = ses.query(Shopping_list)
    for product in q.all():   
        ses.add(Purchased_product(product_id = product.product_id, amount = product.amount, date = date.today()))
    print('Все позиции перенесены в список купленнных товаров')
    clear_shopping_list(ses)
    ses.commit()

def add_product(ses): # добавление продукта
    name = input('Введите наименование продукта: ')
    unit = input('Введите идиницы измерения продукта: ')
    category_list(ses)
    category = int(input('Введите категорию продукта: '))
    # id = len(ses.query(Product).all())+1
    ses.add(Product(name=name, unit=unit, category_id=category))
    ses.commit()

def add_category(ses):
    name = input('Введите название категории: ')
    ses.add(Category(name=name))
    ses.commit()

def add_shopping_list_week(ses):
    product = input('Введите id продукта: ')
    amount = input('Введите количество продукта: ')
    ses.add(Shopping_list_week(product_id=product, amount=amount))
    ses.commit()

def del_shopping_list_week(ses):
    shopping_list_week_view(ses)
    while True:
        name = input('Введите наименование продукта, который нужно удалить из списка: ')
        subq = ses.query(Product).filter(Product.name.like(f'%{name}%')).subquery('sub')
        q = ses.query(subq).join(Shopping_list_week, Shopping_list_week.product_id == subq.c.id)
        count = 0
        for pr in q:
            print(f'{pr.name} - id {pr.id}')
            count += 1
        if count==0:
            choice = input('Совпадений в списке покупок не найдено. Чтобы повторить ввод нажмите введите "y"')
            if choice != 'y':
                break
        else:
            id = input('Введите id товара, который нужно удалить: ')
            ses.query(Shopping_list_week).filter(Shopping_list_week.product_id == id).delete()
            ses.commit()
            break

def update_shopping_list_week(ses):
    shopping_list_week_view(ses)
    while True:
        name = input('Введите наименование продукта, количеество которого нужно изменить: ')
        subq = ses.query(Product).filter(Product.name.like(f'%{name}%')).subquery('sub')
        q = ses.query(subq).join(Shopping_list_week, Shopping_list_week.product_id == subq.c.id)
        count = 0
        for pr in q:
            print(f'{pr.name} - id {pr.id}')
            count += 1
        if count==0:
            choice = input('Совпадений в списке покупок не найдено. Чтобы повторить ввод нажмите введите "y"')
            if choice != 'y':
                break
        else:
            id = input('Введите id товара: ')
            amount = input('Введите необходимое количество товара: ')
            ses.query(Shopping_list_week).filter(Shopping_list_week.product_id == id).update({'amount':amount})
            ses.commit()
            break

def check_products(ses): #проверка продуктов по всему списку и формирование списка покупок
    clear_shopping_list(ses)
    for product in ses.query(Product).all():
        label = 'y'
        while label == 'y':
            label = input(f'{product.name} есть в наличии? (y/n) ')
            if label == 'n':
                amount = float(input(f'Сколько {product.unit} нужно купить? '))
                ses.add(Shopping_list(product_id=product.id, amount=amount))
            elif label !='y':
                print('Ошибка ввода')
                label = 'y'
            else:
                break
    ses.commit()

def check_shopping_list_week(ses): #проверка продуктов по списку на неделю и формирование списка покупок
    clear_shopping_list(ses)
    for product in ses.query(Product).join(Shopping_list_week.product).all(): 
        for pr in product.list_week:
            label = 'y'
            while label == 'y':
                label = input(f'{product.name} есть в наличии? (y/n) ')
                if label == 'n':
                    amount = pr.amount
                    ses.add(Shopping_list(product_id=product.id, amount=amount))
                elif label !='y':
                    print('Ошибка ввода')
                    label = 'y'
                else:
                    break
    ses.commit()

def check_category(ses): #проверка продуктов по категориям
    clear_shopping_list(ses)
    category_list(ses)
    category = input('Введите id выбранной категории: ')
    subq = ses.query(Category).filter(Category.id==category).subquery('sub')
    for product in ses.query(Product).join(subq, subq.c.id == Product.category_id):
        # for pr in product.category:
        label = 'y'
        while label == 'y':
            label = input(f'{product.name} есть в наличии? (y/n) ')
            if label == 'n':
                amount = float(input(f'Сколько {product.unit} нужно купить? '))
                ses.add(Shopping_list(product_id=product.id, amount=amount))
            elif label !='y':
                print('Ошибка ввода')
                label = 'y'
            else:
                break
    ses.commit()




