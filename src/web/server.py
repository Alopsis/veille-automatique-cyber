from flask import Flask, render_template
from pathlib import Path 
from src.article import getSources,getArticles
import os
from datetime import date, timedelta, datetime

app = Flask(__name__, 
            template_folder=Path(__file__).parent / 'website',
            static_folder=Path(__file__).parent / 'website' / 'static' 

)

#@app.route('/company/subdomains/<companyName>', methods=['POST'])
#def servGetSubDomains(companyName):
#    return getSubDomains(companyName)

@app.route('/')
def servIndex():
    print("---------------------")
    print(getSources())
    today = datetime.now()
    seven_days_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')
    return render_template('index.html', sources=getSources(), articles=getArticles(seven_days_ago,today,[]))  

def runWebsite():
    app.run(debug=True)