# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



class User(UserMixin, db.Model):
    """
    Create users table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    userid = db.Column(db.Integer, db.ForeignKey('participants.id'))
    storid = db.Column(db.Integer, db.ForeignKey('storages.id'))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(selfEmployee):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Participant(db.Model):
    """
    Create participants table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model

    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    partname = db.Column(db.String(60), index=True, unique=True)
    fcd = db.Column(db.Float, default=0)
    usd = db.Column(db.Float, default=0)
    sar = db.Column(db.Float, default=0)
    rub = db.Column(db.Float, default=0)
    yen = db.Column(db.Float, default=0)
    users = db.relationship('User', backref='participant', lazy='dynamic')

    def __repr__(self):
        return '<Participant: {}>'.format(self.partname)

class Storage(db.Model):
    """
    Create storages table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model

    __tablename__ = 'storages'

    id = db.Column(db.Integer, primary_key=True)
    storown = db.Column(db.String(60), index=True, unique=True)
    stornum = db.Column(db.Integer, default=0)
    current_capacity = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='storage', lazy='dynamic')

    def __repr__(self):
        return '<Storage: {}>'.format(self.storwown)    