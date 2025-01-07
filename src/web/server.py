from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response  ,jsonify
from pathlib import Path 
import bcrypt 
from src.user import getUser, insertUser
from src.listePerso import insertListe, getListes
from src.article import getSources,getArticles, addArticles
from src.frise import getFrise, addFrise  ,get_specific_frise, addItemToFrise, getItemFrise, getItem
import os
from datetime import date, timedelta, datetime
app = Flask(__name__, 
            template_folder=Path(__file__).parent / 'website',
            static_folder=Path(__file__).parent / 'website' / 'static' 

)
app.secret_key = os.urandom(24)

@app.route('/refresh/articles', methods=['POST'])
def refreshArticles():
    addArticles()
    return "1"
    
@app.route('/add/frise',methods=['POST'])
def addFriseFront():
    nom = request.form.get('nom')
    if not nom:
        return "Le nom de la frise est requis.", 400
    print("Nom de la frise reçu :", nom)
    addFrise(nom)
    return "1"

@app.route('/add/frise/item', methods=['POST'])
def addItemToFriseFront():
    friseid = request.form.get('idfrise')
    valeur = request.form.get('value')
    date = request.form.get('date')
    print("-----------------------------")
    print(friseid)
    print(valeur)
    print(date)
    addItemToFrise(friseid, valeur, date)
    return "1"

@app.route('/item/modify',methods=['POST'])
def modifyItem():
    itemId = request.form.get('itemId')
    return render_template('pages/modifyItem.html',item=getItem(itemId))
@app.route('/valider',methods=['POST'])
def valider():
    sources = request.form.getlist('sources[]')
    print("--------------------------")
    print(sources)
    print("--------------------------")
    today = datetime.now()
    seven_days_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')

    return render_template('pages/articles.html',articles=getArticles(seven_days_ago,today,sources),listesPersos = listePersos)
@app.route('/recup/data/frise',methods=['POST'])
def recupDataForFrise():
    friseId = request.form.get("friseId")
    return getItemFrise(friseId)

@app.route('/affiche/frise',methods=['POST'])
def afficherFriseFront():
    friseId = request.form.get('friseId')
    frise = get_specific_frise(friseId)
    print("-_-_-_-_-_")
    print(frise)
    print(getItemFrise(friseId))
    return render_template('pages/frise.html',frise=frise,itemFrise=getItemFrise(friseId))
@app.route('/')
def servIndex():
    print("---------------------")
    today = datetime.now()
    seven_days_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')
    if 'username' in session:
        username = session['username']
        listePersos = getListes(session['usernameId'])
    else:
        username = None
        listePersos = []
    return render_template('index.html', 
                           sources=getSources(), 
                           articles=getArticles(seven_days_ago, today, []), 
                           frises=getFrise(), 
                           listesPersos=listePersos,
                           username=username)

def runWebsite():
    app.run(debug=True)


@app.route('/add/frisePerso', methods=['POST'])
def ajouteFrisePerso():
    nom = request.form.get('nom')
    insertListe(nom, session["usernameId"])
    return make_response(jsonify({"message": "Login successful"}), 200)  
# Gestion des connexions 

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return make_response(jsonify({"message": "Logout successful"}), 200)  
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = getUser(username, password)

        if user:
            session['username'] = user[1] 
            session['usernameId'] = user[0] 
            return make_response(jsonify({"message": "Login successful"}), 200)  
        else:
            return make_response(jsonify({"message": "Invalid credentials"}), 403)  

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(password)
        user = insertUser(username, password)
        
        if user is None:
            return make_response(jsonify({"message": "Une erreur est apparue"}), 403)  
        else:
            session['username'] = user  # Utilise directement le nom d'utilisateur
            flash('Registration successful!', 'success')
            return make_response(jsonify({"message": "Login successful"}), 200)  


def permPageUser():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    else:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))