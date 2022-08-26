from tkinter.tix import COLUMN
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "AetherVoid.db"
migrate = Migrate()

user_ships = db.Table('user_ships',
    db.Column('neuro_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('ship_id', db.Integer, db.ForeignKey('ship.id')))


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('websiterole.id')))

ship_crew = db.Table('ship_crew',
    db.Column('ship_id', db.Integer, db.ForeignKey('ship.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    currentCredits = db.Column(db.Float(precision=2), default=0.00)
    ships = db.relationship('Ship', secondary=user_ships, backref = 'crewMember')
    userRating = db.Column(db.Float(precision=2), default=0.00)
    ownedArt = db.relationship('Artwork', foreign_keys='Artwork.owner_user_id', backref='ownerUser')
    artistRating = db.Column(db.Float(precision=2), default=0.00)
    createdArt = db.relationship('Artwork', foreign_keys='Artwork.artist_id', backref='artist')
    bills = db.relationship('Bill', backref='billedUser')
    transactions = db.relationship('TransactionLog', backref='transactionUser')
    websiteRoles = db.relationship('WebsiteRole', secondary=user_roles, backref='roleUser')

class WebsiteRole(db.Model):
    __tablename__ = 'websiterole'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False) 

class Ship(db.Model):
    __tablename__ = 'ship'
    id = db.Column(db.Integer, primary_key=True)
    shipName = db.Column(db.String(30), nullable=False)
    maxHP = db.Column(db.Integer, nullable=False)
    currentHP = db.Column(db.Integer, nullable=False)
    crew = db.relationship('User', secondary=ship_crew, backref='crewShip')
    systems = db.relationship('System', backref='ship')
    
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artName = db.Column(db.String(150), nullable=False)
    artImage = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    artRating = db.Column(db.Float(precision=2), default=0)
    purchasePrice = db.Column(db.Float(precision=2), default=0)
    currentPrice = db.Column(db.Float(precision=2), default=0)
    forSale = db.Column(db.Boolean, default=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'),)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priceLog = db.relationship('endDayLog', backref='loggedArtwork')

class vDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    indexDate = db.Column(db.Integer, nullable=False)

class endDayLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))
    worldDate = db.Column(db.String(10))
    indexDate = db.Column(db.Integer)
    closePrice = db.Column(db.Float(precision=2), default=0)

class AccessCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False)

class NeuroxNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    neuroxName = db.Column(db.String(30), nullable=False)

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'))
    systemName = db.Column(db.String(30), nullable=False)
    maxHP = db.Column(db.Integer, nullable=False)
    currentHP = db.Column(db.Integer, nullable=False)
    systemDescription = db.Column(db.String(280), nullable=False)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    worldDate = db.Column(db.String(10))
    indexDate = db.Column(db.Integer)
    balance = db.Column(db.Float(precision=2), default=0)
    transaction = db.Column(db.Float(precision=2), default=0)
    
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    balance = db.Column(db.Float(precision=2), default=0)
    totalBalance = db.Column(db.Float(precision=2), default=0)
    interest = db.Column(db.Float(precision=2), default=0)
    recipient = db.Column(db.String(30), nullable=False)
    nextDueYear = db.Column(db.Integer, nullable=False)
    nextDueDay = db.Column(db.Integer, nullable=False)
    LastPaymentYear = db.Column(db.Integer, nullable=False)
    LastPaymentDay = db.Column(db.Integer, nullable=False)
    isSubscription = db.Column(db.Boolean, default=False)
    isActive = db.Column(db.Boolean, default=False)
    isLate = db.Column(db.Boolean, default=False)






