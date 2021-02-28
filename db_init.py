from collections import namedtuple
from copy import deepcopy

from zapy import db
from zapy.models import Products, Sources

productTuple = namedtuple('productTuple', ['product', 'count', 'source_id'])

sources = ['Lubawa', 'Łasin', 'Bierdronka', 'Lidl', 'Auchan']
products = [
    productTuple('jajka', 20, 1),
    productTuple('winko', 1, 3),
    productTuple('wafle', 2, 4),
]

db.create_all()

for source in sources:
    s = Sources(source_name=source)
    db.session.add(deepcopy(s))

for prod in products:
    p = Products(product=prod.product, count=prod.count, source_id=prod.source_id)
    db.session.add(deepcopy(p))


db.session.commit()
