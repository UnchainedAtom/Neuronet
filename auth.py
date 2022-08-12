from flask import Blueprint, render_template, request, jsonify, redirect, url_for,session, flash
from .database import db, User, Artist, fellCodes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')

        #Query user from database
        user = User.query.filter_by(userName=userName).first()

        #Check user password
        if user:
            if check_password_hash(user.password, password):
                flash('LOGIN SUCCESSFUL', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('LOGIN FAILED', category='error')
        else:
            flash('USER DOES NOT EXIST', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/signUp", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':

        #Get data in forms
        code = request.form.get('code')
        userName = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Verify access code exists in list of codes available 
        exists = db.session.query(fellCodes.id).filter_by(code=code).first() is not None
        print(exists)
            
        #Query user from database
        user = User.query.filter_by(userName=userName).first()
        if not exists:
            flash('ACCESS CODE NOT VALID', category='error')
        elif user:
            flash('USER ALREADY EXISTS', category='error')
        elif len(userName) < 1:
            flash('USERNAME MUST BE GREATER THAN 1 CHARACTER.', category='error')
        elif password1 != password2:
            flash('PASSWORDS DON\'T MATCH.', category='error')
        elif len(password1) < 8:
            flash('PASSWORD MUST BE AT LEAST 8 CHARACTERS.', category='error')
        else:
            new_user = User(userName=userName, password=generate_password_hash(password1, method='sha256'))
            #get code that was matched, so we can delete it 
            matchCode = fellCodes.query.filter_by(code=code).first()
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            db.session.delete(matchCode)
            #Generates artist record to connect to the user, but only turns it on if flag is set.  
            artist = Artist(user_id = new_user.id, artistRating = 0.00)
            db.session.add(artist)
            db.session.commit()
            flash('ACCOUNT CREATED.', category='success')
            return redirect(url_for('views.home'))



    return render_template("signUp.html", user=current_user)