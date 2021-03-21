import json
import time

import flask

from zapy import app, db
from zapy.forms import ProductForm
from zapy.functions import modify_products, get_table_content, get_product_count
from zapy.models import Products, Sources


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ProductForm()
    if form.validate_on_submit():
        cnt = get_product_count(form.product.data)
        product_info = {
            "product": form.product.data,
            "count": max(cnt, 0),
            "in_db": 'Nie' if cnt<0 else 'Tak'
        }
        return flask.render_template('index.html', form=form, product_info=product_info)
    else:
        product_info = {}
        return flask.render_template('index.html', form=form, product_info=product_info)


@app.route('/tabelka', methods = ['GET', 'POST'])
def tabelka():
    if flask.request.method == 'POST':
        jsdata = json.loads(flask.request.get_data(cache=False))[0]
        modify_products(jsdata)
        flask.redirect(flask.url_for('tabelka'))
    table_content = get_table_content()
    return flask.render_template('tabelka.html', table_content=table_content)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('500.html'), 500