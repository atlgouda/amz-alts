from flask import Flask, render_template
from markupsafe import escape
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/results/<term>')
def results(term):
    return render_template('results.html', term=term)
