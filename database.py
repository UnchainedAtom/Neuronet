from tkinter.tix import COLUMN
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "AetherVoid.db"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    userRating = db.Column(db.Float(precision=2), default=0)
    currentCredits = db.Column(db.Float(precision=2), default=0)
    isArtist = db.Column(db.Boolean, default=False)
    isPlayer = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    ownedArt = db.relationship('Artwork', backref='ownerUser')
    artistInfo = db.relationship('Artist', backref='artistUser')
    websiteRoles = db.relationship('WebsiteRole', backref='roleUser')
    
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artName = db.Column(db.String(150), nullable=False)
    artImage = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    artRating = db.Column(db.Float(precision=2), default=0)
    purchasePrice = db.Column(db.Float(precision=2), default=0)
    currentPrice = db.Column(db.Float(precision=2), default=0)
    forSale = db.Column(db.Boolean, default=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priceLog = db.relationship('endDayLog', backref='loggedArtwork')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artistRating = db.Column(db.Float(precision=2), default=0)
    createdArt = db.relationship('Artwork', backref='artist')
    

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


class fellCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False)


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    websiteName = db.Column(db.String(30), nullable=False) 


class WebsiteRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))
    website = db.relationship('Website')
    role = db.Column(db.String(30), nullable=False) 

