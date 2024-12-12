from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Polygon(db.Model):
    __tablename__ = 'polygons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    coordinates = db.Column(db.Text, nullable=False) 
