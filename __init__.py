from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from .database import Bill, NeuroxNode, Ship, System, TransactionLog, WebsiteRole, db, AccessCode, DB_PASSWORD, User, Artwork, vDate, endDayLog, migrate
from .fellViews import fellViews, hasUserRole
from .neuroViews import neuroViews
from .auth import auth
from os import abort, path
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from urllib.parse import quote  


def create_app():
    app = Flask(__name__)
    app.secret_key=('nonprod')

    #OLD SQLlite DATABASE
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    #NEW MySql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/AetherVoid' % quote(DB_PASSWORD)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.permanent_session_lifetime = timedelta(days=1)
    db.init_app(app)
    migrate.init_app(app, db)

    #BLUEPRINTS
    app.register_blueprint(fellViews, url_prefix="/fellowship/")
    app.register_blueprint(neuroViews, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")
 
    #MAX UPLOAD SIZE 16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    create_database(app)

        #LOGIN
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    admin = Admin(app, url='/admin', index_view=HomeAdminView(name='Home'))
    admin.add_views(SecureModelView(User,db.session), SecureModelView(Artwork,db.session), SecureModelView(vDate,db.session),SecureModelView(endDayLog,db.session), SecureModelView(WebsiteRole,db.session), SecureModelView(System,db.session), SecureModelView(TransactionLog,db.session), SecureModelView(Bill,db.session), SecureModelView(Ship,db.session), SecureModelView(NeuroxNode,db.session), SecureModelView(AccessCode,db.session))

        #INJECTING DATE
    @app.context_processor
    def inject_now():
        avDate = vDate.query.get('1')
        formatDate = str(avDate.day) + ':' + str(avDate.year)
        return dict(formatDate=formatDate)

    return app

def create_database(app):
    #if not path.exists(DB_NAME):
    db.create_all(app=app)
    print('CREATED DATABASE')



class SecureModelView(ModelView):

    column_exclude_list = ('artImage')

    def is_accessible(self):
        return hasUserRole(current_user,'ADMIN')
        # return current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('views.home', next=request.url))


class HomeAdminView(AdminIndexView):

    def is_accessible(self):
        return hasUserRole(current_user,'ADMIN')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('views.home'))




