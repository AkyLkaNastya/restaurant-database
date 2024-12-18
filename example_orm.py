auth = {
    'user': 'postgres',
    'password': ''
}


from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('postgresql+psycopg://{}:{}@localhost:5433/georgian_food'.format(auth['user'], auth['password']), echo=True)
metadata = MetaData()


class Staff(Base):
    __tablename__ = 'staff'

    worker_id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String)
    job_title = Column(String)
    address = Column(String)
    phone_number = Column(String)

    def __init__(self, worker_name, job_title, address, phone_number):
        self.worker_name = worker_name
        self.job_title = job_title
        self.address = address
        self.phone_number = phone_number

    def __repr__(self):
        return self.worker_name


class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    serving_waiter = Column(String)
    dish = Column(String)

    def __init__(self, serving_waiter, dish):
        self.serving_waiter = serving_waiter
        self.dish = dish

    def __repr__(self):
        return self.order_id


class OrderPositions(Base):
    __tablename__ = 'order_positions'

    order_id = Column(Integer)
    date = Column(Date)
    total_cost = Column(Float)

    def __init__(self, order_id, date, total_cost):
        self.order_id = order_id
        self.date = date
        self.total_cost = total_cost

    def __repr__(self):
        return self.order_id


class Supllies(Base):
    __tablename__ = 'supllies'

    ingredient = Column(String, primary_key=True)
    supplier_name = Column(String)
    measurement_units = Column(String)
    price_in_usd = Column(Float)

    def __init__(self, ingredient, supplier_name, measurement_units, price_in_usd):
        self.ingredient = ingredient
        self.supplier_name = supplier_name
        self.measurement_units = measurement_units
        self.price_in_usd = price_in_usd

    def __repr__(self):
        return self.ingredient


class Storage(Base):
    __tablename__ = 'storage'

    ingredient = Column(String, primary_key=True)
    ingredient_left = Column(Float)
    max = Column(Float)
    measurement_units_storage = Column(String)

    def __init__(self, ingredient, ingredient_left, max, measurement_units_storage):
        self.ingredient = ingredient
        self.ingredient_left = ingredient_left
        self.max = max
        self.measurement_units_storage = measurement_units_storage

    def __repr__(self):
        return self.ingredient


class Supplier(Base):
    __tablename__ = 'supplier'

    supplier_name = Column(String, primary_key=True)
    city = Column(String)
    delivery = Column(String)
    contact_person = Column(String)

    def __init__(self, supplier_name, city, delivery, contact_person):
        self.supplier_name = supplier_name
        self.city = city
        self.delivery = delivery
        self.contact_person = contact_person

    def __repr__(self):
        return self.supplier_name


class Menu(Base):
    __tablename__ = 'menu'

    dish = Column(String, primary_key=True)
    price_usd = Column(Float)
    rating = Column(Integer)
    stop_list = Column(Integer)

    def __init__(self, dish, price_usd, rating, stop_list):
        self.dish = dish
        self.price_usd = price_usd
        self.rating = rating
        self.stop_list = stop_list

    def __repr__(self):
        return self.dish


class Recipe(Base):
    __tablename__ = 'recipe'

    dish = Column(String, primary_key=True)
    ingredient = Column(String, primary_key=True)
    ing_amount = Column(Float)
    units_of_measurement = Column(String)

    def __init__(self, dish, ingredient, ing_amount, units_of_measurement):
        self.dish = dish
        self.ingredient = ingredient
        self.ing_amount = ing_amount
        self.units_of_measurement = units_of_measurement

    def __repr__(self):
        return self.dish


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine) # bound session
with Session() as session:
    staff_1 = Staff('Fen Waugh', 'Waiter', '123 Main Street Fillory', '+1-555-212-00-78')
    storage_1 = Storage('potato', 2.00, 15.00, 'kilogram')
    menu_1 = Menu('Adzhika', 10.00, 4, False)
    menu_2 = Menu('Pasta', 12.00, 3, True)
    recipe_1 = Recipe('Adzhika', 'flour', 0.01, 'kilogram')
    recipe_2 = Recipe('Adzhika', 'tomato', 0.05, 'kilogram')
    recipe_3 = Recipe('Adzhika', 'salt', 0.001, 'kilogram')
    recipe_4 = Recipe('Adzhika', 'spices mix', 0.002, 'kilogram')


# вызываем функцию в ОРМ стиле
from sqlalchemy import func
with Session() as session:
    # вызовем пользовательскую функцию foo из схемы public
    data = session.query(func.public.foo()).all()

# принтанём результат
for row in data:
    # row - это тапл с одним элементом, который равен одной строке в результате
    print(row[0])
