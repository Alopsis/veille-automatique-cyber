from flask import Flask, render_template
from pathlib import Path 
from ..back.data import *
from ..back.save import *
from ..back.expositionDomains import *
import os
app = Flask(__name__, 
            template_folder=Path(__file__).parent / 'website',
            static_folder=Path(__file__).parent / 'website' / 'static' 

)

@app.route('/company/subdomains/<companyName>', methods=['POST'])
def servGetSubDomains(companyName):
    return getSubDomains(companyName)

@app.route('/company/generate/<companyName>',methods=['POST'])
def servGetNewDomains(companyName):
    if validName(companyName) == 1:
        print("0")
        return "0"
    else:
        print("1")
        searchSubdomains(companyName)
        return "1"
@app.route('/')
def servIndex():
    print(getCompanies())
    return render_template('index.html', companies=getCompanies())  

def runWebsite():
    app.run(debug=True)