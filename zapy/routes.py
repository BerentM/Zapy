import json
import time

import flask

from zapy import app, db, bcrypt
from zapy.forms import ProductForm, RegistrationForm, LoginForm
from zapy.functions import modify_products, get_table_content, get_product_count
from zapy.models import Storage, Shop, Sources


@app.route('/home')
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

@app.route('/tab/<string:page_title>', methods = ['GET', 'POST'])
def tabelka(page_title):
    if page_title not in ('zapasy', 'zakupy'):
        flask.abort(404)
    if flask.request.method == 'POST':
        jsdata = json.loads(flask.request.get_data(cache=False))[0]
        modify_products(jsdata, page_title)
        flask.redirect(flask.url_for('/tab/<str:page_title>'))
    table_content = get_table_content(page_title)
    return flask.render_template('tabelka.html', table_content=table_content, page_title=page_title.capitalize())

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flask.flash(f'Utworzono konto {form.username.data}!', 'success')
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('register.html', page_title='Rejestracja', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@wp.pl' and form.password.data == 'pw':
            flask.flash('Zalogowano pomyślnie!', 'success')
            return flask.redirect(flask.url_for('index'))
        else:
            flask.flash('Logowanie się nie powiodło. Sprawdź nazwę i hasło użytkownika', 'danger')
    return flask.render_template('login.html', page_title='Zaloguj się', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('500.html'), 500