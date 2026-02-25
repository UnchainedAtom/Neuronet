from flask import Blueprint, Response, render_template, request, Response, jsonify, redirect, url_for,session, flash
from database import db, User, Artwork, endDayLog, vDate, AccessCode, TransactionLog
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from sqlalchemy import func
from scipy import stats
import json
import random
import pandas as pd
import numpy as np
import secrets, string

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

fellViews = Blueprint('fellViews', __name__)

#HOME PAGE

@fellViews.route("/")
@login_required
def home():
    return render_template("fellowship/home.html", user=current_user, roles = getAllUserRoles())

@fellViews.route("/profile")
@login_required
def profile():

    isArtist = hasUserRole(current_user,'FELLARTIST')
    print(isArtist)
    if (isArtist):
        return render_template("fellowship/profile.html", user=current_user, roles = getAllUserRoles())

    return render_template("fellowship/profile.html", user=current_user, roles = getAllUserRoles())

#BIG ONE, NEEDS BUY FUNCTION, AND DISPLAY
@fellViews.route("/market")
@login_required
def market():

    artworks=db.session.query(Artwork)

    return render_template("fellowship/market.html", user=current_user, roles = getAllUserRoles(), artworks=artworks)

#NEEDS TO SHOW WHAT USERS OWN, AND ADD SELL FUNCTION
@fellViews.route("/inventory")
@login_required
def inventory():
    """#GOOD TEST EXAMPLES OF MODEL TRAVERSAL
    for art in current_user.ownedArt:
        print(art)
        print(art.ownerUser.artistInfo[0].artistRating)
        print(art.artist.artistUser.userName)
    """

    return render_template("fellowship/inventory.html", user=current_user, roles = getAllUserRoles())

#SHOULD BE ABLE TO CHANGE DATE AND MAYBE ADD EXTRA ADMIN FUNCTION PAGE IN HERE
#added more securtiy, need to check if user is admin here as well
@fellViews.route("/myAdmin")
@login_required
def myAdmin():
    isAdmin = hasUserRole(current_user,'ADMIN')
    if isAdmin:

        currentDate = vDate.query.get(1)
        return render_template("fellowship/myAdmin.html", user=current_user, roles = getAllUserRoles(), currentDate = currentDate)

    return redirect(url_for('fellViews.home'))


#TODO NEED TO DO FIGURE OUT A METHOD TO MAKE SURE ONLY JPG,PNGS,and OTHER IMAGE FORMATS ARE ALLOWED
@fellViews.route("/artist", methods=['GET', 'POST'])
@login_required
def artist():
    # Only allow users with the FELLARTIST role
    if not hasUserRole(current_user, 'FELLARTIST'):
        flash('You do not have permission to upload artwork.', category='error')
        return redirect(url_for('fellViews.home'))

    if request.method == 'POST':
        artImage = request.files.get('artImage')
        artName = request.form.get('artName')
        artPrice = request.form.get('artPrice')

        if not artImage or not artName or not artPrice:
            flash('All fields are required.', category='error')
            return redirect(url_for('fellViews.artist'))

        if not allowed_file(artImage.filename):
            flash('MUST BE PNG, JPG, JPEG, OR GIF', category='error')
            return redirect(url_for('fellViews.artist'))

        mimetype = artImage.mimetype
        if not mimetype.startswith('image/'):
            flash('Invalid file type.', category='error')
            return redirect(url_for('fellViews.artist'))

        try:
            price = float(artPrice)
        except ValueError:
            flash('Invalid price.', category='error')
            return redirect(url_for('fellViews.artist'))

        img = Artwork(
            artName=artName,
            artImage=artImage.read(),
            mimetype=mimetype,
            currentPrice=price,
            artist_id=current_user.id,
            owner_user_id=current_user.id
        )
        db.session.add(img)
        db.session.commit()

        flash('UPLOAD SUCCESS', category='success')
        return redirect(url_for('fellViews.artist'))

    return render_template("fellowship/artist.html", user=current_user, roles=getAllUserRoles())

# What actually gets the image
@fellViews.route("/<int:id>")
@login_required
def get_img(id):
    img = Artwork.query.get(id)
    return Response(img.artImage, mimetype=img.mimetype)


# sells artwork
@fellViews.route("/sell-artwork", methods=['POST'])
@login_required
def sell_artwork():
    print('IN SELL')
    artwork = json.loads(request.data)
    artworkId = artwork['artworkId']
    artwork = Artwork.query.get(artworkId)

    #adds credits to user based on price of artwork when sold
    #artwork is now owned by Fellowship Market, and no longer belongs to user
    if artwork:
        if artwork.ownerUser.id == current_user.id:
            #current_user.currentCredits = uCredits+artPrice
            #artwork.owner_user_id = fellowshipMarket.id
            #artwork.purchasePrice = artPrice
            artwork.forSale = True
            db.session.commit()

    return jsonify({})

# buys artwork
@fellViews.route("/buy-artwork", methods=['POST'])
@login_required
def buy_artwork():
    artwork = json.loads(request.data)
    artworkId = artwork['artworkId']
    artwork = Artwork.query.get(artworkId)
    artist=artwork.artist

    #get currentOwner
    currentOwner=artwork.ownerUser

    if artwork:
        if currentOwner.id != current_user.id:

            uCredits = current_user.currentCredits
            oCredits = currentOwner.currentCredits
            artPrice = artwork.currentPrice
            userRating = currentOwner.userRating
            artRating = artwork.artRating
            artistRating = artist.artistRating

            #checks if user credits are greater than the price of the piece
            if uCredits >= artPrice:

                current_user.currentCredits = uCredits-artPrice

                #gives the current Owner of the art piece the credits
                currentOwner.currentCredits = oCredits + artPrice
                currentOwner.userRating = userRating + ((random.randint(1,3))/100)
                artwork.artRating = artRating + ((random.randint(1,2))/100)
                artist.artistRating = artistRating + ((random.randint(1,2))/100)


                artwork.owner_user_id = current_user.id
                artwork.purchasePrice = artPrice
                artwork.forSale = False
                
                #Log Transaction
                currentDate = vDate.query.get(1)
                iDate = currentDate.indexDate
                wDate = str(currentDate.day) + ':' + str(currentDate.year)

                #BUYER
                balance = current_user.currentCredits
                transaction = -abs(artPrice)                
                buyLog = TransactionLog(user_id=current_user.id , worldDate=wDate, indexDate=iDate, balance=balance, transaction=transaction)
                db.session.add(buyLog)

                #SELLER
                balance = currentOwner.currentCredits
                transaction = abs(artPrice)
                sellLog = TransactionLog(user_id=currentOwner.id , worldDate=wDate, indexDate=iDate, balance=balance, transaction=transaction)
                db.session.add(sellLog)

                db.session.commit()
            else:
                flash('NOT ENOUGH CREDITS')
        else:
            flash('CANNOT BUY ART YOU ALREADY OWN', category='error')

    return jsonify({})


# Next Day
@fellViews.route("/next-day", methods=['POST'])
@login_required
def next_day():
    voidDate = vDate.query.get(1)
    marketArt = db.session.query(Artwork).filter(Artwork.forSale == True )
    allArt = db.session.query(Artwork).all()
    artPrices = [a.currentPrice for a in db.session.query(Artwork.currentPrice)]
    artAvg = stats.trim_mean(artPrices, 0.2)
    maxArtPrice = (artAvg * 3) 

    # NPC buyers for the market (simulated market activity)
    npc_buyers = [
        'Collector_Vex',
        'TradeMaster_Zyn', 
        'Investor_Kael',
        'GalleryScan_IX',
        'Curator_Nyx'
    ]

    #Go through all artworks still for sale, and decided if they get bought
    for artwork in marketArt:
        print()
        print(artwork.artName)
        
        buyArt=0
        currentOwner=artwork.ownerUser
        artist=artwork.artist
        
        # Get or create NPC buyers for market simulation
        potentialBuyers = []
        for npc_name in npc_buyers:
            npc = User.query.filter_by(userName=npc_name).first()
            if npc:
                potentialBuyers.append(npc)
        
        # Don't include the current owner in potential buyers
        potentialBuyers = [buyer for buyer in potentialBuyers if buyer.id != currentOwner.id]
        
        buyerListLen = len(potentialBuyers) - 1 if potentialBuyers else -1
        
        print(f"NPC Buyers available: {len(potentialBuyers)}")
        print(potentialBuyers)

        if buyerListLen < 0:
            buyerListLen = 0

        #Calculate artwork percent buy
        percentBuy = (((currentOwner.userRating * .05) + (artist.artistRating * .15) + (artwork.artRating * .20) + ( (random.randint(1,100)) * .25) + (100 * .35))/100)
        print('Percent BUY:' + str(percentBuy))


        #logic to evaluate if the artowrk is worth buying
        if artwork.currentPrice <= maxArtPrice and (random.random() < percentBuy):
            buyArt=1
            print('bought!')
            print()

        print('BUY LIST LEN' + str(buyerListLen))
        #if buy go through list of NPCs and randomly assign this to one.  Treat like an art buy
        if buyArt==1 and buyerListLen > 0:

            randomUser = potentialBuyers[(random.randint(0,buyerListLen))]
            print(randomUser)
            
            
            if artwork:
                if currentOwner.id != randomUser.id:

                    oCredits = currentOwner.currentCredits
                    artPrice = artwork.currentPrice
                    userRating = currentOwner.userRating
                    artRating = artwork.artRating
                    artistRating = artist.artistRating

                    #gives the current Owner of the art piece the credits,
                    #increase current owner score for sell, increase artRating for buy, increase artist score for trade
                    currentOwner.currentCredits = oCredits + artPrice
                    currentOwner.userRating = userRating + ((random.randint(1,3))/100)
                    artwork.artRating = artRating + ((random.randint(1,2))/100)
                    artist.artistRating = artistRating + ((random.randint(1,2))/100)
                    
                    #Sets purchasing user to new owner, updates last purchase price, sets the artwork back for sale
                    artwork.owner_user_id = randomUser.id
                    artwork.purchasePrice = artPrice
                    artwork.forSale = True

                    #Log Transaction
                    currentDate = vDate.query.get(1)
                    iDate = currentDate.indexDate
                    wDate = str(currentDate.day) + ':' + str(currentDate.year)

                    #SELLER
                    balance = currentOwner.currentCredits
                    transaction = abs(artPrice)
                    sellLog = TransactionLog(user_id=currentOwner.id , worldDate=wDate, indexDate=iDate, balance=balance, transaction=transaction)
                    db.session.add(sellLog)


        #if no buy, change for sale tag back to False.  User will have to decide to sell again for the next day
        elif hasUserRole(current_user, 'PLAYER') == True:
            artwork.forSale = False

    #Change Prices for the next day
    
    #Go through every artwork and log the closing prices for the day
    logPrices(allArt)
    db.session.commit()

    #Actual new price Calculations
    priceChange(allArt)
    db.session.commit()




    #increment the day
    if (voidDate.day + 1) < 361:
        voidDate.day = voidDate.day + 1 
    else:
        voidDate.day = 1
        voidDate.year = voidDate.year + 1

    #Increment the index day
    voidDate.indexDate = voidDate.indexDate + 1

    db.session.commit()
    return jsonify({})

def priceChange(allArt):
    for artwork in allArt:
        query=db.session.query(endDayLog).filter(endDayLog.art_id == artwork.id)
        # Get the results directly instead of using pd.read_sql
        logs = query.all()
        
        # Convert to DataFrame if there are logs
        if logs:
            df = pd.DataFrame([(log.indexDate, log.closePrice) for log in logs], columns=['indexDate', 'closePrice'])
            df = df.sort_values('indexDate').reset_index(drop=True)
        else:
            df = pd.DataFrame(columns=['indexDate', 'closePrice'])
        
        returns = np.log(1 + df['closePrice'].pct_change())
        mu, sigma = returns.mean(), returns.std()

        #accounts for new art not having any movement
        if sigma == 0 or np.isnan(sigma):
            sigma = (random.randint(1, 4) / 100) + (random.random() / 100)
        
        if np.isnan(mu):
            mu = 0
            
        sim_rets = np.random.normal(mu, sigma, 1)
        print(df)
        if df.empty:
            currentP = artwork.currentPrice
        else: 
            currentP = df['closePrice'].iloc[-1]
        print(sigma)
        print(mu)
        print(artwork.artName)
        print(sim_rets)
        newPrice = float(currentP * (sim_rets + 1).cumprod()[0])
        if newPrice < 0:
            newPrice = 0.00
        
        artwork.currentPrice = round(newPrice, 2)
        

    return

def logPrices(allArt):
    for artwork in allArt:
        currentPrice = artwork.currentPrice
        currentDate = vDate.query.get(1)
        iDate = currentDate.indexDate
        wDate = str(currentDate.day) + ':' + str(currentDate.year)
        

        artLog = endDayLog(art_id=artwork.id , worldDate=wDate, indexDate=iDate, closePrice=currentPrice)
        db.session.add(artLog)
    

    return



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hasUserRole(user,ROLE):
    roleList=current_user.query.filter(User.websiteRoles.any( role = ROLE )).all()
    if user in roleList:
        
        return True
    else:
        
        return False

def getAllUserRoles():
    roles = []
    for role in current_user.websiteRoles:
        roles.append(role.role)
    return roles




# generate access code
@fellViews.route("/gen-code", methods=['POST'])
@login_required
def gen_code():
    genCode = (''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(15)))
    addCode = AccessCode(code=genCode)
    db.session.add(addCode)
    db.session.commit()
    return jsonify({})

@fellViews.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash('File too large. Max size is 16MB.', category='error')
    return redirect(url_for('fellViews.artist'))