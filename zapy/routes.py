import json

import flask

from zapy import app, db
from zapy.forms import NameForm
from zapy.functions import modify_products
from zapy.models import Products, Sources


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = flask.session.get('name')
        if old_name is not None and old_name != form.name.data:
            if form.name.data == 'Mateusz':
                flask.flash('Witaj mistrzu')
            else:
                flask.flash('Name has been changed.')
        flask.session['name'] = form.name.data
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('index.html', form=form, name=flask.session.get('name'))

@app.route('/user/<name>')
def user(name):
    kwargs = {
        'name': name,
        'ip': flask.request.remote_addr
    }
    posts = [
        {
        "author": "Mateusz",
        "title": "VPN + RaspberryPi",
        "date": "2021-02-01"
        },
        {
        "author": "Mateusz",
        "title": "Jaki len z wiskozą kupić?",
        "date": "2021-02-01"
        }
    ]
    return flask.render_template('user.html', **kwargs, posts=posts)


@app.route('/tabelka', methods = ['GET', 'POST'])
def tabelka():
    if flask.request.method == 'POST':
        jsdata = json.loads(flask.request.get_data(cache=False))[0]
        modify_products(jsdata)
    results = db.session.query(Products, Sources).join(Sources).all()
    table_content = [{
        "id": result.Products.id,
        "product": result.Products.product,
        "count": result.Products.count,
        "source": result.Sources.source_name,
        "added": result.Products.timestamp.strftime('%Y-%m-%d')
    } for result in results]

    return flask.render_template('tabelka.html', table_content=table_content)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('500.html'), 500