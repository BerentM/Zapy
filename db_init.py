from collections import namedtuple
from copy import deepcopy

from zapy import db
from zapy.models import Storage, Sources, Shop, User

product_tuple = namedtuple('product_tuple', ['product', 'count', 'source_id', 'user_id'])
user_tuple = namedtuple('user_tuple', ['username', 'email', 'password'])

sources = ['Lubawa', 'Łasin', 'Bierdronka', 'Lidl', 'Auchan']
products = [
    product_tuple('jajka', 20, 1, 1),
    product_tuple('winko', 1, 3, 1),
    product_tuple('wafle', 2, 4, 2),
]

shopping_list = [
    product_tuple('piwo', 6, 3, 1)
]

users = [
    user_tuple('Mateusz', 'mateusz@test.pl', 'haslo1'),
    user_tuple('Kinga', 'kinga@test.pl', 'haslo2'),
]

db.create_all()

for user in users:
    p = User(username=user.username, email=user.email, password=user.password)
    db.session.add(deepcopy(p))

for source in sources:
    s = Sources(source_name=source)
    db.session.add(deepcopy(s))

for prod in products:
    p = Storage(product=prod.product, count=prod.count, source_id=prod.source_id, user_id=prod.user_id)
    db.session.add(deepcopy(p))

for prod in shopping_list:
    p = Shop(product=prod.product, count=prod.count, source_id=prod.source_id, user_id=prod.user_id)
    db.session.add(deepcopy(p))

db.session.commit()
