from flask import Flask, render_template, redirect, request, url_for
import requests
from markupsafe import escape
from forms import SearchForm
from bs4 import BeautifulSoup
import html2text

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
    # CLUBHOUSE INFO
    source = requests.get('https://www.clubhousekidandcraft.com/search?q={}'.format(term)).text
    soup = BeautifulSoup(source, "html.parser")
    soup.prettify(formatter='html')
    thumbnails = soup.findAll("div", {"class": "one-fifth"})
    linx = []
    alts = []
    sites= []
    for t in thumbnails:
        imgs = t.findAll("img")
        if len(imgs) > 0:
            for image in imgs:
                n = str(image).split(" src=\"")
                if len(n) > 1:
                    link = n[1][:-9]
                    linx.append(link)
                    a = str(image).split("alt=\"")
                    alt = str(a).split("\"")[0][11:]
                    alts.append(alt)
            anchors = t.findAll("a")
            for anchor in anchors:
                i = str(anchor).split("<a href=\"")
                if len(i) > 1:
                    j = str(i[1]).split("\" title=")[0]
                    sites.append(j) 
    # RHEN'S NEST INFO
    rnsource = requests.get('https://rhensnesttoyshop.com/search?type=product&options%5Bprefix%5D=last&q={}'.format(term)).text
    rnsoup = BeautifulSoup(rnsource, "html.parser")
    rnsoup.prettify(formatter='html')
    rnthumbnails = rnsoup.findAll("div", {"class":"rimage-wrapper"})
    rnlinx = []
    rnalts = []
    rnsites = []
    for t in rnthumbnails:
        imgs = t.findAll("img")
        if len(imgs)> 0:
            for image in imgs:
                n = str(image).split("data-src=\"")
                if len(n)>1:
                    link = n[1].split("{width}x.jpg")[0]
                    rnlinx.append(link)
                    # print(rnlinx)
    rntitles = rnsoup.findAll("div", {"class":"product-block__title"})
    for title in rntitles:
        if len(title)>0:
            x = str(title).split("ss=r\">")[1]
            rnalt = str(x).split("</a>")[0]
            rnalts.append(rnalt)

    # print('RHENS NEST')
    # print(rnsource)
    Html_file = open("raw.html", "w")
    Html_file.write(str(rnthumbnails))
    Html_file.close()
    return render_template('results.html', term=term, thumbnails=thumbnails, 
            linx=linx, alts=alts, sites=sites,
            rnlinx=rnlinx, rnalts=rnalts
            )
