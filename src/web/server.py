from flask import Flask, render_template
from pathlib import Path 
from src.article import getSources
import os
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
    return render_template('index.html', sources=getSources())  

def runWebsite():
    app.run(debug=True)