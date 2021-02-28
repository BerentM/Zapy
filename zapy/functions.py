from zapy import db
from zapy.models import Products, Sources


def find_source_id(js):
    def query(js):
        return db.session.query(Sources).filter(Sources.source_name == js['Source']).first()

    if source_row := query(js):
        return source_row.id
    else:
        db.session.add(Sources(source_name=js['Source']))
        db.session.commit()
        source_row = query(js)
        return source_row.id

def modify_products(js):
    if js['OperationType'] == 'Edit':
        if existing := db.session.query(Products).filter(Products.id == js['Id']).first():
            print(existing)
            existing.product = js['Product']
            existing.count = js['Count']
            existing.source_id = find_source_id(js)
            db.session.commit()
        else:
            p = Products(product=js['Product'], count=js['Count'], source_id=find_source_id(js))
            db.session.add(p)
            db.session.commit()
    elif js['OperationType'] == 'Delete':
        if existing := db.session.query(Products).filter(Products.id == js['Id']).first():
            db.session.delete(existing)
            db.session.commit()

