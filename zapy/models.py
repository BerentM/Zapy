import datetime

from zapy import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(120), unique=True, nullable=False)
    count = db.Column(db.Integer)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.product}':'{self.count}', '{self.timestamp}')"

class Sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    product = db.relationship('Products', backref='sources', lazy='joined')

    def __repr__(self):
        return f"Source('{self.id}':'{self.source_name}', '{self.timestamp}')"