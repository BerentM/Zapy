from zapy import db
from zapy.models import Products, Sources


def find_source_id(js):
    def query(js):
        return db.session.query(Sources).filter(Sources.source_name == js['Source']).first()
    
    def add_new_source(js):
        db.session.add(Sources(source_name=js['Source']))
        db.session.commit()

    if source_row := query(js):
        return source_row.id
    else:
        add_new_source(js)
        source_row = query(js)
        return source_row.id

def modify_products(js):
    if js['OperationType'] == 'Edit':
        if existing := db.session.query(Products).filter(Products.product == js['Product']).first():
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

def get_table_content():
    results = db.session.query(Products, Sources).join(Sources).all()
    tmp_content = [{
        "id": result.Products.id,
        "product": result.Products.product,
        "count": result.Products.count,
        "source": result.Sources.source_name,
        "added": result.Products.timestamp.strftime('%Y-%m-%d')
    } for result in results]
    # empty row for adding new things to list
    table_content = [{
        "id": '',
        "product": '',
        "count": '',
        "source": '',
        "added": ''
    }]

    if tmp_content:
        table_content.extend(tmp_content)

    return table_content

def get_product_count(product_input):
    result = db.session.query(Products).filter(Products.product == product_input).first()
    
    return result.count if result else -999