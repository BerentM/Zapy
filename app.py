import json

import flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('Jak masz na imie?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = flask.Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'super tajne haslo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/zapy.db'

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

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

if __name__ == '__main__':
    app.run(debug=True)
