from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LasbcaEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cn = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    contravention = db.Column(db.Text, nullable=False)
    action_taken = db.Column(db.Text, nullable=False)
    picture_1_filename = db.Column(db.String(255), nullable=True) # First image string reference
    picture_2_filename = db.Column(db.String(255), nullable=True) # Second image string reference
