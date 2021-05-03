import datetime

from zapy import db

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(120), unique=True, nullable=False)
    count = db.Column(db.Integer)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"shopping_list('{self.product}':'{self.count}', '{self.timestamp}')"

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(120), unique=True, nullable=False)
    count = db.Column(db.Integer)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"storage_list('{self.product}':'{self.count}', '{self.timestamp}')"

class Sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    product = db.relationship('Storage', backref='sources', lazy='joined')
    product = db.relationship('Shop', backref='sources', lazy='joined')

    def __repr__(self):
        return f"source_list('{self.id}':'{self.source_name}', '{self.timestamp}')"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"