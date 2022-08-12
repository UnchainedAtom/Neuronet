from flask import Blueprint, Response, render_template, request, Response, jsonify, redirect, url_for,session, flash
from .database import db, User, Artist, Artwork, endDayLog, vDate, fellCodes
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
from scipy import stats
import json
import random
import pandas as pd
import numpy as np
import secrets, string

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

views = Blueprint('views', __name__)

#HOME PAGE

@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/profile")
@login_required
def profile():
    if current_user.isArtist:
        artistUser = db.session.query(User, Artist).join(Artist).filter(User.id == current_user.id).first()
        return render_template("profile.html", user=current_user, artist=artistUser[1])

    return render_template("profile.html", user=current_user)

#BIG ONE, NEEDS BUY FUNCTION, AND DISPLAY
@views.route("/market")
@login_required
def market():

    artworks=db.session.query(Artwork)

    return render_template("market.html", user=current_user, artworks=artworks)

#NEEDS TO SHOW WHAT USERS OWN, AND ADD SELL FUNCTION
@views.route("/inventory")
@login_required
def inventory():

    """#GOOD TEST EXAMPLES OF MODEL TRAVERSAL
    for art in current_user.ownedArt:
        print(art)
        print(art.ownerUser.artistInfo[0].artistRating)
        print(art.artist.artistUser.userName)
    """

    return render_template("inventory.html", user=current_user)

#SHOULD BE ABLE TO CHANGE DATE AND MAYBE ADD EXTRA ADMIN FUNCTION PAGE IN HERE
#added more securtiy, need to check if user is admin here as well
@views.route("/myAdmin")
@login_required
def myAdmin():
    if current_user.isAdmin:

        currentDate = vDate.query.get('1')
        return render_template("myAdmin.html", user=current_user, currentDate = currentDate)

    return redirect(url_for('views.home'))


#TODO NEED TO DO FIGURE OUT A METHOD TO MAKE SURE ONLY JPG,PNGS,and OTHER IMAGE FORMATS ARE ALLOWED
@views.route("/artist", methods=['GET', 'POST'])
@login_required
def artist():
    #deals with artwork upload
    if request.method == 'POST':
        
        artistUser = db.session.query(User, Artist).join(Artist).filter(User.id == current_user.id).first()

        artImage = request.files['artImage']
        artName = request.form.get('artName')
        artPrice = request.form.get('artPrice')
        print(artPrice)

        #error with upload, flash and redirect back
        if not artImage:
            flash('UPLOAD ERROR', category='error')
            return redirect(url_for('views.artist'))

        if artImage and allowed_file(artImage.filename):
            #artFilename = secure_filename(artImage.artFilename)
            mimetype = artImage.mimetype

            #makes the image to be submitted to the database
            img = Artwork(artName=artName, artImage=artImage.read(), mimetype=mimetype, currentPrice=artPrice, artist_id=artistUser[1].id, owner_user_id = current_user.id)
            db.session.add(img)
            db.session.commit()

            flash('UPLOAD SUCCESS', category='success')
            return redirect(url_for('views.artist'))

        else:
            flash('MUST BE PNG, JPG, JPEG, OR GIF', category='error')
            return redirect(url_for('views.artist'))

    #loads page for artist
    if current_user.isArtist:
        artistUser = db.session.query(User, Artist).join(Artist).filter(User.id == current_user.id).first()
        return render_template("artist.html", user=current_user, artist=artistUser[1])

    return redirect(url_for('views.home'))


# What actually gets the image
@views.route("/<int:id>")
@login_required
def get_img(id):
    img = Artwork.query.get(id)
    return Response(img.artImage, mimetype=img.mimetype)


# sells artwork
@views.route("/sell-artwork", methods=['POST'])
@login_required
def sell_artwork():
    artwork = json.loads(request.data)
    artworkId = artwork['artworkId']
    artwork = Artwork.query.get(artworkId)
    fellowshipMarket = User.query.get('1')
    uCredits = current_user.currentCredits
    artPrice = artwork.currentPrice

    #adds credits to user based on price of artwork when sold
    #artwork is now owned by Fellowship Market, and no longer belongs to user
    if artwork:
        if artwork.owner_user_id == current_user.id:
            #current_user.currentCredits = uCredits+artPrice
            #artwork.owner_user_id = fellowshipMarket.id
            #artwork.purchasePrice = artPrice
            artwork.forSale = True
            db.session.commit()

    return jsonify({})

# buys artwork
@views.route("/buy-artwork", methods=['POST'])
@login_required
def buy_artwork():
    artwork = json.loads(request.data)
    artworkId = artwork['artworkId']
    artwork = Artwork.query.get(artworkId)
    artist=artwork.artist

    #get currentOwner ID
    currentOwner=artwork.ownerUser



    if artwork:
        if artwork.owner_user_id != current_user.id:

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
                db.session.commit()
            else:
                flash('NOT ENOUGH CREDITS')
        else:
            flash('CANNOT BUY ART YOU ALREADY OWN', category='error')

    return jsonify({})


# Next Day
@views.route("/next-day", methods=['POST'])
@login_required
def next_day():
    voidDate = vDate.query.get('1')
    marketArt = db.session.query(Artwork).filter(Artwork.forSale == True )
    allArt = db.session.query(Artwork).all()
    artPrices = [a.currentPrice for a in db.session.query(Artwork.currentPrice)]
    artAvg = stats.trim_mean(artPrices, 0.2)
    maxArtPrice = (artAvg * 3) 
    print(artPrices)
    print(artAvg)
    print()

    #Go through all artworks still for sale, and decided if they get bought
    for artwork in marketArt:
        print()
        print(artwork.artName)
        
        buyArt=0
        currentOwner=artwork.ownerUser
        artist=artwork.artist
        potentialBuyers=db.session.query(User).filter(User.isPlayer == False and User.id!=currentOwner.id).all()
        buyerListLen = (len(potentialBuyers)-1)

        if buyerListLen < 0:
            buyerListLen = 0

        print(potentialBuyers)

        #Calculate artwork percent buy
        percentBuy = (((currentOwner.userRating * .05) + (artist.artistRating * .25) + (artwork.artRating * .30) + ( (random.randint(1,100)) * .40))/100)
        print(percentBuy)


        #TODO logic to evaluate if the artowrk is worth buying
        if artwork.currentPrice <= maxArtPrice and (random.random() < percentBuy):
            buyArt=1
            print('bought!')
            print()

        #TODO if buy go through list of NPCs and randomly assign this to one.  Treat like an art buy
        if buyArt==1 and buyerListLen > 0:

            randomUser = potentialBuyers[(random.randint(0,buyerListLen))]
            
            
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


        #if no buy, change for sale tag back to False.  User will have to decide to sell again for the next day
        elif currentOwner.isPlayer == True:
            artwork.forSale = False

    #TODO Change Prices for the next day
    
    #Go through every artwork and log the closing prices for the day
    logPrices(allArt)
    #db.session.commit()

    #Actual new price Calculations
    priceChange(allArt)




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
        df = pd.read_sql(query.statement, query.session.bind)
        df.sort_values('indexDate')
        returns = np.log(1+ df['closePrice'].pct_change())
        mu,sigma = returns.mean(), returns.std()

        #accounts for new art not having any movement
        if sigma == 0 or np.isnan(sigma)  :
            sigma =  (random.randint(1,4)/100) + (random.random()/100)
        
        if np.isnan(mu)  :
            mu = 0
            
        sim_rets = np.random.normal(mu,sigma,1)
        print(df)
        if df.empty:
            currentP = artwork.currentPrice
        else: 
            currentP = df['closePrice'].iloc[-1]
        print(sigma)
        print(mu)
        print(artwork.artName)
        print(sim_rets)
        print(float(currentP * (sim_rets + 1).cumprod()))
        newPrice = float(currentP * (sim_rets + 1).cumprod())
        if newPrice < 0:
            newPrice = 0.00
        
        artwork.currentPrice = round(newPrice, 2)
        

    return

def logPrices(allArt):
    for artwork in allArt:
        currentPrice = artwork.currentPrice
        currentDate = vDate.query.get('1')
        iDate = currentDate.indexDate
        wDate = str(currentDate.day) + ':' + str(currentDate.year)
        

        artLog = endDayLog(art_id=artwork.id , worldDate=wDate, indexDate=iDate, closePrice=currentPrice)
        db.session.add(artLog)
    

    return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# generate access code
@views.route("/gen-code", methods=['POST'])
@login_required
def gen_code():
    genCode = (''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(15)))
    addCode = fellCodes(code=genCode)
    db.session.add(addCode)
    db.session.commit()
    return jsonify({})