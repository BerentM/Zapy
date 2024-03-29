from zapy import db
from zapy.models import Storage, Shop, Sources


def select_class(table):
    if table == 'zapasy':
        return Storage
    elif table == 'zakupy':
        return Shop

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

def modify_products(js, table):
    Tab = select_class(table)
    if js['OperationType'] == 'Edit':
        if existing := db.session.query(Tab).filter(Tab.id == js['Id']).first():
            existing.product = js['Product']
            existing.count = js['Count']
            existing.source_id = find_source_id(js)
            db.session.commit()
        else:
            p = Tab(product=js['Product'], count=js['Count'], source_id=find_source_id(js))
            db.session.add(p)
            db.session.commit()
    elif js['OperationType'] == 'Delete':
        if existing := db.session.query(Tab).filter(Tab.id == js['Id']).first():
            db.session.delete(existing)
            db.session.commit()

def get_table_content(table):
    Tab = select_class(table)
    results = db.session.query(Tab, Sources).join(Sources).all()
    if table == 'zapasy':
        tmp_content = [{
            "id": result.Storage.id,
            "product": result.Storage.product,
            "count": result.Storage.count,
            "source": result.Sources.source_name,
            "added": result.Storage.timestamp.strftime('%Y-%m-%d')
        } for result in results]
    elif table == 'zakupy':
        tmp_content = [{
            "id": result.Shop.id,
            "product": result.Shop.product,
            "count": result.Shop.count,
            "source": result.Sources.source_name,
            "added": result.Shop.timestamp.strftime('%Y-%m-%d')
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
    result = db.session.query(Storage).filter(db.func.lower(Storage.product) == db.func.lower(product_input)).first()
    
    return result.count if result else -999