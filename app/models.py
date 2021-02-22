from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db
    with app.app_context():
        app.db.create_all() 


class DIDNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(30))
    monthy_price = db.Column(db.Float(precision=(8,2), asdecimal=True))
    setup_price = db.Column(db.Float(precision=(8,2), asdecimal=True))
    currency = db.Column(db.String(3))