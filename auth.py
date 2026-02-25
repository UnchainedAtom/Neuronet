from flask import Blueprint, render_template, request, jsonify, redirect, url_for,session, flash
from database import db, User, AccessCode, PlayerAbilitySave, PlayerSkill, WebsiteRole
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
                return redirect(url_for('neuroViews.home'))
            else: 
                flash('LOGIN FAILED', category='error')
        else:
            flash('USER DOES NOT EXIST', category='error')

    return render_template("neuronet/login.html", user=current_user)

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
        exists = db.session.query(AccessCode.id).filter_by(code=code).first() is not None
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
            new_user = User(userName=userName, password=generate_password_hash(password1))
            #get code that was matched, so we can delete it 
            matchCode = AccessCode.query.filter_by(code=code).first()
            db.session.add(new_user)
            db.session.commit()
            
            # Assign role based on access code
            if code.upper() == 'ADMIN-001':
                admin_role = WebsiteRole.query.filter_by(role='ADMIN').first()
                fellartist_role = WebsiteRole.query.filter_by(role='FELLARTIST').first()
                if admin_role:
                    new_user.websiteRoles.append(admin_role)
                if fellartist_role:
                    new_user.websiteRoles.append(fellartist_role)
            else:
                # Assign FELLARTIST role by default for regular users
                fellartist_role = WebsiteRole.query.filter_by(role='FELLARTIST').first()
                if fellartist_role:
                    new_user.websiteRoles.append(fellartist_role)
            
            login_user(new_user, remember=True)
            createStats(new_user)
            current_user.baseAC = 10
            db.session.delete(matchCode)
            db.session.commit()
            flash('ACCOUNT CREATED.', category='success')
            return redirect(url_for('neuroViews.home'))



    return render_template("neuronet/signUp.html", user=current_user)


def createStats(nUser):
    #CREATE SAVES
    strSave = PlayerAbilitySave(abilityModifier='STR',user_id=nUser.id)
    dexSave = PlayerAbilitySave(abilityModifier='DEX',user_id=nUser.id)
    conSave = PlayerAbilitySave(abilityModifier='CON',user_id=nUser.id)
    intSave = PlayerAbilitySave(abilityModifier='INT',user_id=nUser.id)
    wisSave = PlayerAbilitySave(abilityModifier='WIS',user_id=nUser.id)
    chaSave = PlayerAbilitySave(abilityModifier='CHA',user_id=nUser.id)

    db.session.add(strSave)
    db.session.add(dexSave)
    db.session.add(conSave)
    db.session.add(intSave)
    db.session.add(wisSave)
    db.session.add(chaSave)

    #CREATE SKILLS
    dexSkill = PlayerSkill(abilityModifier='DEX', name='ACROBATICS', user_id=nUser.id)
    animHandSkill = PlayerSkill(abilityModifier='WIS', name='ANIMAL HANDLING', user_id=nUser.id)
    arcanaSkill = PlayerSkill(abilityModifier='INT', name='ARCANA', user_id=nUser.id)
    athSkill = PlayerSkill(abilityModifier='STR', name='ATHLETICS', user_id=nUser.id)
    decSkill = PlayerSkill(abilityModifier='CHA', name='DECEPTION', user_id=nUser.id)
    dataSkill = PlayerSkill(abilityModifier='INT', name='DATA', user_id=nUser.id)
    histSkill = PlayerSkill(abilityModifier='INT', name='HISTORY', user_id=nUser.id)
    insightSkill = PlayerSkill(abilityModifier='WIS', name='INSIGHT', user_id=nUser.id)
    intimSkill = PlayerSkill(abilityModifier='CHA', name='INTIMIDATION', user_id=nUser.id)
    investSkill = PlayerSkill(abilityModifier='INT', name='INVESTIGATION', user_id=nUser.id)
    medSkill = PlayerSkill(abilityModifier='WIS', name='MEDICINE', user_id=nUser.id)
    natSkill = PlayerSkill(abilityModifier='INT', name='NATURE', user_id=nUser.id)
    percepSkill = PlayerSkill(abilityModifier='WIS', name='PERCEPTION', user_id=nUser.id)
    pilotSkill = PlayerSkill(abilityModifier='DEX', name='PILOTING', user_id=nUser.id)
    religSkill = PlayerSkill(abilityModifier='INT', name='RELIGION', user_id=nUser.id)
    sohSkill = PlayerSkill(abilityModifier='DEX', name='SLEIGHT OF HAND', user_id=nUser.id)
    stealthSkill = PlayerSkill(abilityModifier='DEX', name='STEALTH', user_id=nUser.id)
    survSkill = PlayerSkill(abilityModifier='WIS', name='SURVIVAL', user_id=nUser.id)
    techSkill = PlayerSkill(abilityModifier='INT', name='TECH', user_id=nUser.id)


    db.session.add(dexSkill)
    db.session.add(animHandSkill)
    db.session.add(arcanaSkill)
    db.session.add(athSkill)
    db.session.add(decSkill)
    db.session.add(dataSkill)
    db.session.add(histSkill)
    db.session.add(insightSkill)
    db.session.add(intimSkill)
    db.session.add(investSkill)
    db.session.add(medSkill)
    db.session.add(natSkill)
    db.session.add(percepSkill)
    db.session.add(pilotSkill)
    db.session.add(religSkill)
    db.session.add(sohSkill)
    db.session.add(stealthSkill)
    db.session.add(survSkill)
    db.session.add(techSkill)


    return