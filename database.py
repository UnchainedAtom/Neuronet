from tkinter.tix import COLUMN
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
import os

db = SQLAlchemy()
DB_NAME = "AetherVoid"
DB_PASSWORD = os.environ['MYSQL_PASSWORD']
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
# weapon_attachments = db.Table('weapon_attachments',
#     db.Column('weapon_id', db.Integer, db.ForeignKey('playerweapon.id')),
#     db.Column('attachment_id', db.Integer, db.ForeignKey('attachment.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    #INFO
    userName = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    realName = db.Column(db.String(50))
    homeworld = db.Column(db.String(50))
    species = db.Column(db.String(50))
    age = db.Column(db.Integer, default=0)
    currentCredits = db.Column(db.Float(precision=2), default=0.00)

    #HP I think we can keep
    maxHP = db.Column(db.Integer, default=0, nullable=False)
    maxOverrideHP = db.Column(db.Integer, default=0, nullable=False)
    currentHP = db.Column(db.Integer, default=0)
    tmpHP = db.Column(db.Integer, default=0)

    #ARMOR KILL THIS
    baseAC = db.Column(db.Integer, default=0)
    acAbility1 = db.Column(db.String(3))
    acAbility2 = db.Column(db.String(3))
    bonusAC = db.Column(db.Integer, default=0)
    overrideAC = db.Column(db.Integer, default=0) 
    currentAC = db.Column(db.Integer, default=0) #Kill this one
    armor = db.relationship('PlayerArmor', backref='armorUser')
    
    #ABILITIES  KILL THIS
    strScore = db.Column(db.Integer, default=0)
    strBonus = db.Column(db.Integer, default=0)
    strOverride = db.Column(db.Integer, default=0)
    dexScore = db.Column(db.Integer, default=0)
    dexBonus = db.Column(db.Integer, default=0)
    dexOverride = db.Column(db.Integer, default=0)
    conScore = db.Column(db.Integer, default=0)
    conBonus = db.Column(db.Integer, default=0)
    conOverride = db.Column(db.Integer, default=0)
    intScore = db.Column(db.Integer, default=0)
    intBonus = db.Column(db.Integer, default=0)
    intOverride = db.Column(db.Integer, default=0)
    wisScore = db.Column(db.Integer, default=0)
    wisBonus = db.Column(db.Integer, default=0)
    wisOverride = db.Column(db.Integer, default=0)
    chaScore = db.Column(db.Integer, default=0)
    chaBonus = db.Column(db.Integer, default=0)
    chaOverride = db.Column(db.Integer, default=0)
    profScore = db.Column(db.Integer, default=0)

    #SAVES KILL THIS
    saves = db.relationship('PlayerAbilitySave', backref='saveUser')

    #SKILLS KILL THIS
    skills = db.relationship('PlayerSkill', backref='skillUser')

    #SPEED KILL THIS
    walkingSpeed = db.Column(db.Integer, default=0)
    flyingSpeed = db.Column(db.Integer, default=0)
    swimmingSpeed = db.Column(db.Integer, default=0)
    climbingSpeed = db.Column(db.Integer, default=0)

    #INITIATIVE KILL THIS
    initBonus = db.Column(db.Integer, default=0)
    initOverride = db.Column(db.Integer, default=0)

    #EQUIPMENT KILL THIS
    equipment = db.relationship('PlayerEquipment', backref='equipmentUser')

    #WEAPONS MAYBE MAKE A REGISTRY
    weapons = db.relationship('PlayerWeapon', backref='weaponUser')

    #SHIPS LEANING TOWARDS KEEP
    ships = db.relationship('Ship', secondary=user_ships, backref = 'crewMember')

    #FELLOWSHIP
    userRating = db.Column(db.Float(precision=2), default=0.00)
    ownedArt = db.relationship('Artwork', foreign_keys='Artwork.owner_user_id', backref='ownerUser')
    artistRating = db.Column(db.Float(precision=2), default=0.00)
    createdArt = db.relationship('Artwork', foreign_keys='Artwork.artist_id', backref='artist')

    #BANK
    bills = db.relationship('Bill', backref='billedUser')
    transactions = db.relationship('TransactionLog', backref='transactionUser')

    #ROLES
    websiteRoles = db.relationship('WebsiteRole', secondary=user_roles, backref='roleUser')

class WebsiteRole(db.Model):
    __tablename__ = 'websiterole'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False) 

#Think we keep
class Ship(db.Model):
    __tablename__ = 'ship'
    id = db.Column(db.Integer, primary_key=True)
    shipName = db.Column(db.String(30), nullable=False)
    maxHP = db.Column(db.Integer, default=0, nullable=False)
    currentHP = db.Column(db.Integer, default=0, nullable=False)
    crew = db.relationship('User', secondary=ship_crew, backref='crewShip')
    systems = db.relationship('System', backref='ship')
    
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artName = db.Column(db.String(150), nullable=False)
    artImage = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    artRating = db.Column(db.Float(precision=2), default=0)
    purchasePrice = db.Column(db.Float(precision=2), default=0)
    currentPrice = db.Column(db.Float(precision=2), default=0)
    forSale = db.Column(db.Boolean, default=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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

#ships are complicated, unsure if worth the effort, later addition
class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'))
    systemName = db.Column(db.String(30), nullable=False)
    maxHP = db.Column(db.Integer, nullable=False)
    currentHP = db.Column(db.Integer, nullable=False)
    systemDescription = db.Column(db.String(280), nullable=False)
# I think bills could be fun to work our, keeps roleplay 
class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    worldDate = db.Column(db.String(10))
    indexDate = db.Column(db.Integer)
    balance = db.Column(db.Float(precision=2), default=0)
    transaction = db.Column(db.Float(precision=2), default=0)
# I think bills could be fun to work our, keeps roleplay    
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




#leaning towards kill
class WeaponTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

#leaning towards kill, or registry overhaul
class PlayerWeapon(db.Model):
    __tablename__ = 'playerweapon'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20)) 
    isProficient = db.Column(db.Boolean, default=False)
    isEquipped = db.Column(db.Boolean, default=False)
    isRanged = db.Column(db.Boolean, default=False)
    isThrown = db.Column(db.Boolean, default=False)
    isVersatile = db.Column(db.Boolean, default=False)
    isFinesse = db.Column(db.Boolean, default=False)
    isTwoHanded = db.Column(db.Boolean, default=False)
    isLight = db.Column(db.Boolean, default=False)
    isHeavy = db.Column(db.Boolean, default=False)
    isConcealable = db.Column(db.Boolean, default=False)
    isFist = db.Column(db.Boolean, default=False)
    isScatter = db.Column(db.Boolean, default=False)
    isAutomatic = db.Column(db.Boolean, default=False)
    isMounted = db.Column(db.Boolean, default=False)
    isNonlethal = db.Column(db.Boolean, default=False)
    isForegrip = db.Column(db.Boolean, default=False)
    isFirearm = db.Column(db.Boolean, default=False)
    hasHeat = db.Column(db.Boolean, default=False)
    hasAmmo = db.Column(db.Boolean, default=False)
    isSpecial = db.Column(db.Boolean, default=False)
    attunementRequired = db.Column(db.Boolean, default=False)
    isattuned = db.Column(db.Boolean, default=False)
    reach = db.Column(db.Integer, default=0)
    shortRange = db.Column(db.Integer, default=0)
    longRange = db.Column(db.Integer, default=0)
    weaponBonus = db.Column(db.Integer, default=0)
    baseDamageDice = db.Column(db.String(20))
    baseDamageBonus = db.Column(db.Integer, default=0)
    versatileDamageDice = db.Column(db.String(20))
    versatileDamageBonus = db.Column(db.Integer, default=0)
    baseDamageType =  db.Column(db.String(20))
    bonusDamageDice = db.Column(db.String(20))
    bonusDamageType = db.Column(db.String(20))
    attachment_id = db.Integer, db.ForeignKey('attachment.id')
    attachments = db.relationship('Attachment', backref='weapon')

#leaning towards kill  
class ArmorTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

#leaning towards kill
class PlayerArmor(db.Model):
    __tablename__ = 'playerarmor'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isProficient = db.Column(db.Boolean, default=False)
    isEquipped = db.Column(db.Boolean, default=False)
    baseAC = db.Column(db.Integer, default=0)
    armorType = db.Column(db.String(3))
    acAbility1 = db.Column(db.String(3))
    acAbility2 = db.Column(db.String(3))

#leaning towards kill
class EquipmentTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

#Unsure.  Maybe registry, leaning towards kill
class PlayerEquipment(db.Model):
    __tablename__ = 'playerequipment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isEquipped = db.Column(db.Boolean, default=False)
    isAmmo = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Integer, default=1)

#KILL this
class PlayerSkill(db.Model):
    __tablename__ = 'playerskill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    isProficient = db.Column(db.Boolean, default=False)
    abilityModifier = db.Column(db.String(3))
    bonus = db.Column(db.Integer, default=0)
    overrideSkill = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#KILL this
class PlayerAbilitySave(db.Model):
    __tablename__ = 'playerabilitysave'
    id = db.Column(db.Integer, primary_key=True)
    overrideSave = db.Column(db.Integer, default=0)
    isProficient = db.Column(db.Boolean, default=False)
    bonus = db.Column(db.Integer, default=0)
    abilityModifier = db.Column(db.String(3))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#Unsure, don't think I want weapons in here at all possibly.  Maybe just a regisrty for weapons
class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    weapon_id = db.Column(db.Integer, db.ForeignKey('playerweapon.id'))
    name = db.Column(db.String(20)) 
    desc = db.Column(db.String(256)) 



