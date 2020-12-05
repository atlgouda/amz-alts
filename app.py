from flask import Flask, render_template, redirect, request, url_for, send_from_directory
from forms import SearchForm
from bs4 import BeautifulSoup
import sys
import os
from stores import clubhouse, chItemList, rhens, rItemList, bkItemList, brave, scrapeSites, kzItemList, kazoo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jlusOUmDgSVJWKOMr3eT'

@app.route('/', methods=['POST', 'GET'])
def search():
    form = SearchForm(request.form)
    if form.is_submitted():
        term = form.term.data
        return redirect(url_for('results', term=term))
    return render_template('home.html', form=form)

@app.route('/results/<term>')
def results(term):
    scrapeSites(term)
    # Html_file = open("raw.html", "w")
    # Html_file.write(str(bksoup))
    # Html_file.close()

    return render_template('results.html', term=term,
            rItemList=rItemList, bkItemList=bkItemList,
            # blItemList=blItemList, 
            kzItemList = kzItemList, chItemList=chItemList
            )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')