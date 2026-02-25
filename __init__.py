from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from database import Bill, NeuroxNode, Ship, System, TransactionLog, WebsiteRole, db, AccessCode, User, Artwork, vDate, endDayLog, migrate
from fellViews import fellViews, hasUserRole
from neuroViews import neuroViews
from auth import auth
from os import abort, path
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from config import current_config


def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(current_config)
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
        try:
            avDate = vDate.query.get(1)
            if avDate:
                formatDate = str(avDate.day) + ':' + str(avDate.year)
            else:
                formatDate = "0:0"  # Default if no date exists
        except:
            formatDate = "0:0"  # Default on any error
        return dict(formatDate=formatDate)

    return app

def create_database(app):
    """Create database tables if they don't exist"""
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("If this is your first run, please run: python init_db.py")



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




