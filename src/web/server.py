from flask import Flask, render_template, request
from pathlib import Path 
from src.article import getSources,getArticles, addArticles
from src.frise import getFrise, addFrise  ,get_specific_frise, addItemToFrise, getItemFrise, getItem
import os
from datetime import date, timedelta, datetime
app = Flask(__name__, 
            template_folder=Path(__file__).parent / 'website',
            static_folder=Path(__file__).parent / 'website' / 'static' 

)

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

    return render_template('pages/articles.html',articles=getArticles(seven_days_ago,today,sources))
@app.route('//recup/data/frise',methods=['POST'])
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
    return render_template('index.html', sources=getSources(), articles=getArticles(seven_days_ago,today,[]), frises=getFrise())  

def runWebsite():
    app.run(debug=True)