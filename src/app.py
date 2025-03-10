from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from db import connect_db, get_objects, add_object, update_object, delete_object

app = Flask(__name__)
db = connect_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/players')
def players():
    players = get_objects(db, 'players')
    return render_template('players.html', players=players)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player_route():
    if request.method == 'POST':
        player = {
            "username": request.form['username'],
            "combat_level": request.form['combat_level'],
            "account_type": request.form['account_type']
        }
        add_object(db, 'players', player)
        return redirect(url_for('players'))
    return render_template('add_player.html')

@app.route('/player/<player_id>')
def player(player_id):
    player = db['players'].find_one({"_id": ObjectId(player_id)})
    return render_template('player.html', player=player)

@app.route('/edit_player/<player_id>', methods=['GET', 'POST'])
def edit_player_route(player_id):
    if request.method == 'POST':
        player = {
            "username": request.form['username'],
            "combat_level": request.form['combat_level'],
            "account_type": request.form['account_type']
        }
        update_object(db, 'players', player_id, player)
        return redirect(url_for('players'))
    player = db['players'].find_one({"_id": ObjectId(player_id)})
    return render_template('edit_player.html', player=player)

@app.route('/delete_player/<player_id>')
def delete_player_route(player_id):
    delete_object(db, 'players', player_id)
    return redirect(url_for('players'))

@app.route('/listings')
def listings():
    listings = get_objects(db, 'listings')
    return render_template('listings.html', listings=listings)

@app.route('/add_listing', methods=['GET', 'POST'])
def add_listing_route():
    if request.method == 'POST':
        listing = {
            "player_id": ObjectId(request.form['player_id']),
            "item_name": request.form['item_name'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "purchased": request.form['purchased'].lower() == 'true',
            "tags": request.form['tags'].split(',')
        }
        add_object(db, 'listings', listing)
        return redirect(url_for('listings'))
    players = get_objects(db, 'players')
    return render_template('add_listing.html', players=players)

@app.route('/edit_listing/<listing_id>', methods=['GET', 'POST'])
def edit_listing_route(listing_id):
    if request.method == 'POST':
        listing = {
            "player_id": ObjectId(request.form['player_id']),
            "item_name": request.form['item_name'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "purchased": request.form['purchased'].lower() == 'true',
            "tags": request.form['tags'].split(',')
        }
        update_object(db, 'listings', listing_id, listing)
        return redirect(url_for('listings'))
    listing = db['listings'].find_one({"_id": ObjectId(listing_id)})
    players = get_objects(db, 'players')
    return render_template('edit_listing.html', listing=listing, players=players)

@app.route('/delete_listing/<listing_id>')
def delete_listing_route(listing_id):
    delete_object(db, 'listings', listing_id)
    return redirect(url_for('listings'))

@app.route('/player_listings/<player_id>')
def player_listings_route(player_id):
    listings = db['listings'].find({"player_id": ObjectId(player_id)})
    player = db['players'].find_one({"_id": ObjectId(player_id)})
    return render_template('player_listings.html', listings=listings, player=player)

if __name__ == '__main__':
    app.run(debug=True)