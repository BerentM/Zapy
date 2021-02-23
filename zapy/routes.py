import json

import flask

from zapy import app
from zapy.forms import NameForm
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

products = [
    {
        "id": 1,
        "product": "popkorn",
        "count": 2,
        "source": "Auchan",
        "added": "2021-02-21",
    },
    {
        "id": 2,
        "product": "sztućce",
        "count": 1,
        "source": "Auchan",
        "added": "2021-02-21",
    },
    {
        "id": 3,
        "product": "jajka",
        "count": 40,
        "source": "Lubawa",
        "added": "2021-02-21",
    },
]


@app.route('/tabelka')
def tabelka():
    return flask.render_template('tabelka.html', products=products)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('500.html'), 500

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = flask.request.get_data(cache=False)
    print(json.loads(jsdata))
    return jsdata