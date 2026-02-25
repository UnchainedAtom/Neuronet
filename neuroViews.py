from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from database import PlayerArmor, db, User, Artwork, endDayLog, vDate, AccessCode, TransactionLog
from flask_login import login_required, current_user
from sqlalchemy import and_
import secrets, string

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

neuroViews = Blueprint('neuroViews', __name__)

@neuroViews.route("/")
@login_required
def home():
    abilityDict = calcCurrentAbilities()
    savesDict = calcCurrentSaves(abilityDict)
    currentAC=calculateAC(abilityDict)


    return render_template("neuronet/home.html", user=current_user, roles = getAllUserRoles(), abilityDict=abilityDict, savesDict=savesDict, currentAC=currentAC)

@neuroViews.route("/baseline")
@login_required
def baseline():
    abilityDict = calcCurrentAbilities()
    skillDict = calcCurrentSkills(abilityDict)
    currentAC=calculateAC(abilityDict)


    return render_template("neuronet/baseline.html", user=current_user, roles = getAllUserRoles(), abilityDict=abilityDict, skillDict=skillDict, currentAC=currentAC)

@neuroViews.route("/neurox")
@login_required
def neurox():
    """Neurox hub page - gateway to all subsystems"""
    return render_template("neuronet/neurox.html", user=current_user, roles=getAllUserRoles())


#Adjusts base Max HP and override Max HP 
@neuroViews.route("/submitVitals" , methods=['POST'])
@login_required
def submitVitals():
    maxHP =  int(request.form['maxHP'])
    maxOverrideHP = int(request.form['maxOverrideHP'])
    currentHP = int(current_user.currentHP)
    tmpHP = int(current_user.tmpHP)

    if maxHP < 0:
        maxHP = 0

    if currentHP > maxHP:
        current_user.currentHP = maxHP
        currentHP = maxHP
    elif (maxOverrideHP > 0) and (currentHP > maxOverrideHP):
        current_user.currentHP = maxOverrideHP
        currentHP = maxOverrideHP
        
    current_user.maxHP = maxHP
    current_user.maxOverrideHP = maxOverrideHP
    db.session.commit()
    return jsonify({'maxHP':maxHP, 'maxOverrideHP':maxOverrideHP, 'newHP':currentHP, 'tmpHP':tmpHP})

#Heals hp
@neuroViews.route("/healVitals" , methods=['POST'])
@login_required
def healVitals():
    healHP =  int(request.form['healHP'])
    
    if healHP < 0:
        healHP=0

    #gets current HP only, not taking into account tmp, since you cant heal tmp HP
    currentHP = current_user.currentHP
    tmpHP = current_user.tmpHP
    
    #check for override max
    if current_user.maxOverrideHP > 0:
        maxHP = current_user.maxOverrideHP
    else:
        maxHP = current_user.maxHP
    
    newHP = currentHP + healHP

    #Check if hp is greated than max
    if newHP > maxHP:
        newHP=maxHP
    
    current_user.currentHP = newHP
    
    db.session.commit()
    return jsonify({'newHP':newHP, 'tmpHP':tmpHP})


#Damages hp
@neuroViews.route("/damageVitals" , methods=['POST'])
@login_required
def damageVitals():

    damageHP =  int(request.form['damageHP'])
    
    if damageHP < 0:
        damageHP=0
    #gets current HP and tmpHP
    currentHP = current_user.currentHP
    tmpHP = current_user.tmpHP

    #accounts for tmp HP logic.  Should damage tmp HP first, then subtract that from the damage
    if tmpHP > 0:
        newTmpHP = tmpHP - damageHP
        damageHP = damageHP - tmpHP
        if newTmpHP < 0:
            newTmpHP = 0
        if damageHP < 0:
            damageHP = 0
    else:
        newTmpHP = tmpHP
    

            
    newHP = currentHP - damageHP

    #Check if hp is less than 0, set it to 0
    if newHP < 0:
        newHP=0
    
    current_user.tmpHP = newTmpHP
    current_user.currentHP = newHP
    
    db.session.commit()
    return jsonify({'newHP':newHP, 'tmpHP':newTmpHP})

#sets tmp hp
@neuroViews.route("/tmpVitals" , methods=['POST'])
@login_required
def tmpVitals():
    tmpHP =  int(request.form['tmpHP'])
    #gets current HP
    currentHP = current_user.currentHP
    if tmpHP < 0:
        tmpHP=0

    #enters new tmpHP into database
    current_user.tmpHP = tmpHP


    db.session.commit()
    return jsonify({'currentHP':currentHP, 'tmpHP':tmpHP})

#submits ability scores
@neuroViews.route("/submitAbilities" , methods=['POST'])
@login_required
def submitAbilities():

    #sets to 0 if above and puts into database
    current_user.strScore =  minZero(int(request.form['strBase']))
    current_user.strOverride =  minZero(int(request.form['strOverride']))
    current_user.dexScore =  minZero(int(request.form['dexBase']))
    current_user.dexOverride =  minZero(int(request.form['dexOverride']))
    current_user.conScore =  minZero(int(request.form['conBase']))
    current_user.conOverride =  minZero(int(request.form['conOverride']))
    current_user.intScore =  minZero(int(request.form['intBase']))
    current_user.intOverride =  minZero(int(request.form['intOverride']))
    current_user.wisScore =  minZero(int(request.form['wisBase']))
    current_user.wisOverride =  minZero(int(request.form['wisOverride']))
    current_user.chaScore =  minZero(int(request.form['chaBase']))
    current_user.chaOverride =  minZero(int(request.form['chaOverride']))

    db.session.commit()
    return jsonify({})

@neuroViews.route("/submitAC" , methods=['POST'])
@login_required
def submitAC():

    #sets to 0 if above and puts into database
    current_user.baseAC =  minZero(int(request.form['baseAC']))
    current_user.acAbility1 =  request.form['ability1']
    current_user.acAbility2 =  request.form['ability2']
    current_user.overrideAC =  minZero(int(request.form['overrideAC']))

    db.session.commit()
    return jsonify({})

@neuroViews.route("/submitInfo" , methods=['POST'])
@login_required
def submitInfo():

    #sets to 0 if above and puts into database
    current_user.realName =  request.form['nameInfo']
    current_user.species =  request.form['speciesInfo']
    current_user.age =  minZero(int(request.form['ageInfo']))
    current_user.homeworld =  request.form['homeworldInfo']

    db.session.commit()
    return jsonify({})


@neuroViews.route("/submitQuickBar" , methods=['POST'])
@login_required
def submitQuickBar():

    #sets to 0 if above and puts into database
    current_user.walkingSpeed =  minZero(int(request.form['walkSpeed']))
    current_user.flyingSpeed =  minZero(int(request.form['flySpeed']))
    current_user.swimmingSpeed =  minZero(int(request.form['swimSpeed']))
    current_user.climbingSpeed =  minZero(int(request.form['climbSpeed']))
    current_user.initOverride =  minZero(int(request.form['initOverride']))
    current_user.profScore =  minZero(int(request.form['profBonus']))
    

    db.session.commit()
    return jsonify({})


#submits ability Saves
@neuroViews.route("/submitSaves" , methods=['POST'])
@login_required
def submitSaves():

    #sets to 0 if below and puts into database
    strProf = request.form['strProf']
    strOverride =  minZero(int(request.form['strOverride']))
    dexProf =  request.form['dexProf']
    dexOverride =  minZero(int(request.form['dexOverride']))
    conProf =  request.form['conProf']
    conOverride =  minZero(int(request.form['conOverride']))
    intProf =   request.form['intProf']
    intOverride =  minZero(int(request.form['intOverride']))
    wisProf =   request.form['wisProf']
    wisOverride =  minZero(int(request.form['wisOverride']))
    chaProf =   request.form['chaProf']
    chaOverride =  minZero(int(request.form['chaOverride']))
    print(strProf)
    print(dexProf)

    for save in current_user.saves:

        if save.abilityModifier == 'STR':
            if strProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if strOverride > 0:
                save.overrideSave = strOverride
            else:
                save.overrideSave = 0
        
        elif save.abilityModifier == 'DEX':
            if dexProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if dexOverride > 0:
                save.overrideSave = dexOverride
            else:
                save.overrideSave = 0

        elif save.abilityModifier == 'CON':
            if conProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if conOverride > 0:
                save.overrideSave = conOverride
            else:
                save.overrideSave = 0

        elif save.abilityModifier == 'INT':
            if intProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if intOverride > 0:
                save.overrideSave = intOverride
            else:
                save.overrideSave = 0

        elif save.abilityModifier == 'WIS':
            if wisProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if wisOverride > 0:
                save.overrideSave = wisOverride
            else:
                save.overrideSave = 0

        elif save.abilityModifier == 'CHA':
            if chaProf == 'true':
                save.isProficient = 1
            else:
                save.isProficient = 0

            if chaOverride > 0:
                save.overrideSave = chaOverride
            else:
                save.overrideSave = 0
        


    db.session.commit()
    return jsonify({})

def getAllUserRoles():
    roles = []
    for role in current_user.websiteRoles:
        roles.append(role.role)
    return roles

def calcCurrentAbilities():

    abilityDict = {}

    #STRENGTH
    if current_user.strOverride > 0:
        strScore = current_user.strOverride
        strMod = (strScore - 10)//2
    else:
        strScore = current_user.strScore + current_user.strBonus
        strMod = (strScore - 10)//2

    #DEXTERITY
    if current_user.dexOverride > 0:
        dexScore = current_user.dexOverride
        dexMod = (dexScore - 10)//2
    else:
        dexScore = current_user.dexScore + current_user.dexBonus
        dexMod = (dexScore - 10)//2
        
    #CONSTITUTION
    if current_user.conOverride > 0:
        conScore = current_user.conOverride
        conMod = (conScore - 10)//2
    else:
        conScore = current_user.conScore + current_user.conBonus
        conMod = (conScore - 10)//2

    #INTELLIGENCE
    if current_user.intOverride > 0:
        intScore = current_user.intOverride
        intMod = (intScore - 10)//2
    else:
        intScore = current_user.intScore + current_user.intBonus
        intMod = (intScore - 10)//2

    #WISDOM
    if current_user.wisOverride > 0:
        wisScore = current_user.wisOverride
        wisMod = (wisScore - 10)//2
    else:
        wisScore = current_user.wisScore + current_user.wisBonus
        wisMod = (wisScore - 10)//2

    #CHARISMA
    if current_user.chaOverride > 0:
        chaScore = current_user.chaOverride
        chaMod = (chaScore - 10)//2
    else:
        chaScore = current_user.chaScore + current_user.chaBonus
        chaMod = (chaScore - 10)//2

    abilityDict["STR"] = [strScore, strMod]
    abilityDict["DEX"] = [dexScore, dexMod]
    abilityDict["CON"] = [conScore, conMod]
    abilityDict["INT"] = [intScore, intMod]
    abilityDict["WIS"] = [wisScore, wisMod]
    abilityDict["CHA"] = [chaScore, chaMod]

    return abilityDict


def calcCurrentSaves(abilityDict):
    savesDict = {}

    for save in current_user.saves:
        #STRENGTH
        if save.abilityModifier == 'STR':
            if save.overrideSave > 0:
                strSave = save.overrideSave
                savesDict["STR"] = [strSave, False]
            else:
                if save.isProficient:
                    strSave = (abilityDict["STR"][1]) + save.bonus + current_user.profScore
                    savesDict["STR"] = [strSave, True]
                else:
                    strSave = (abilityDict["STR"][1]) + save.bonus
                    savesDict["STR"] = [strSave, False]

        #DEXTERITY
        if save.abilityModifier == 'DEX':
                if save.overrideSave > 0:
                    dexSave = save.overrideSave
                    savesDict["DEX"] = [dexSave, False]
                else:
                    if save.isProficient:
                        dexSave = (abilityDict["DEX"][1]) + save.bonus + current_user.profScore
                        savesDict["DEX"] = [dexSave, True]
                    else:
                        dexSave = (abilityDict["DEX"][1]) + save.bonus
                        savesDict["DEX"] = [dexSave, False]

        #CONSTITUTION
        if save.abilityModifier == 'CON':
            if save.overrideSave > 0:
                conSave = save.overrideSave
                savesDict["CON"] = [conSave, False]
            else:
                if save.isProficient:
                    conSave = (abilityDict["CON"][1]) + save.bonus + current_user.profScore
                    savesDict["CON"] = [conSave, True]
                else:
                    conSave = (abilityDict["CON"][1]) + save.bonus
                    savesDict["CON"] = [conSave, False]

        #INTELLIGENCE
        if save.abilityModifier == 'INT':
            if save.overrideSave > 0:
                intSave = save.overrideSave
                savesDict["INT"] = [intSave, False]
            else:
                if save.isProficient:
                    intSave = (abilityDict["INT"][1]) + save.bonus + current_user.profScore
                    savesDict["INT"] = [intSave, True]
                else:
                    intSave = (abilityDict["INT"][1]) + save.bonus
                    savesDict["INT"] = [intSave, False]
    
        #WISDOM
        if save.abilityModifier == 'WIS':
            if save.overrideSave > 0:
                wisSave = save.overrideSave
                savesDict["WIS"] = [wisSave, False]
            else:
                if save.isProficient:
                    wisSave = (abilityDict["WIS"][1]) + save.bonus + current_user.profScore
                    savesDict["WIS"] = [wisSave, True]
                else:
                    wisSave = (abilityDict["WIS"][1]) + save.bonus
                    savesDict["WIS"] = [wisSave, False]
    
        #CHARISMA
        if save.abilityModifier == 'CHA':
            if save.overrideSave > 0:
                chaSave = save.overrideSave
                savesDict["CHA"] = [chaSave, False]
            else:
                if save.isProficient:
                    chaSave = (abilityDict["CHA"][1]) + save.bonus + current_user.profScore
                    savesDict["CHA"] = [chaSave, True]
                else:
                    chaSave = (abilityDict["CHA"][1]) + save.bonus
                    savesDict["CHA"] = [chaSave, False]




    return savesDict

def calcCurrentSkills(abilityDict):
    skillsDict = {}

    for skill in current_user.skills:
        
        #STRENGTH
        if skill.abilityModifier == 'STR':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["STR"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["STR"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]

        #DEXTERITY
        if skill.abilityModifier == 'DEX':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["DEX"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["DEX"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]

        #CONSTITUTION
        if skill.abilityModifier == 'CON':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["CON"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["CON"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]

        #INTELIGENCE
        if skill.abilityModifier == 'INT':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["INT"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["INT"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]

        
        #WISDOM
        if skill.abilityModifier == 'WIS':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["WIS"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["WIS"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]

                
        #CHARISMA
        if skill.abilityModifier == 'CHA':
            if skill.overrideSkill > 0:
                skillMod = skill.overrideSkill
                skillsDict[skill.name] = [skillMod, False]
            else:
                if skill.isProficient:
                    skillMod = (abilityDict["CHA"][1]) + skill.bonus + current_user.profScore
                    skillsDict[skill.name] = [skillMod, True]
                else:
                    skillMod = (abilityDict["CHA"][1]) + skill.bonus
                    skillsDict[skill.name] = [skillMod, False]
        
        

    return skillsDict    

#Calculate AC based on whether wearing armor or not
def calculateAC(abilityDict):
        
    armor =  db.session.query(PlayerArmor).filter(and_(PlayerArmor.user_id==current_user.id, PlayerArmor.isEquipped==1)).first()
    bonusAC = current_user.bonusAC
    overrideAC = current_user.overrideAC
    mod1=0
    mod2=0

    if armor:
        base = armor.baseAC
        armorType = armor.armorType
        acAbility1 = armor.acAbility1
        acAbility2 = armor.acAbility2
        
        #get mod bonus for AC
        if acAbility1:
            mod1 = abilityDict[acAbility1][1]
        if acAbility2:
            mod2 = abilityDict[acAbility2][1]

        match armorType:
            case 'LIT':
                currentAC = base + mod1 + bonusAC
            case 'MED':
                if mod1 > 2:
                    mod1 = 2
                currentAC = base + mod1 + bonusAC
            case 'HEV':
                 currentAC = base + bonusAC
        
        print(currentAC)

    
    else:
        #
        base = current_user.baseAC
        acAbility1 = current_user.acAbility1
        acAbility2 = current_user.acAbility2

        #get mod bonus for AC
        if acAbility1:
            mod1 = abilityDict[acAbility1][1]
        if acAbility2:
            mod2 = abilityDict[acAbility2][1]

        currentAC = base + mod1 + mod2 + bonusAC
        print(currentAC)

    #Check if needed to override AC
    if overrideAC > 0:
        currentAC = overrideAC

    return currentAC

def minZero(number):
    if number < 0:
        number = 0
    return number