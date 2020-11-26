from flask import Flask, render_template, redirect, request, url_for
import requests
from markupsafe import escape
from forms import SearchForm
from bs4 import BeautifulSoup
import sys
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
    class rItem():
        def __init__(self, rImg, rTitle, rLink, rPrice):
            self.rImg = rImg
            self.rTitle = rTitle
            self.rLink = rLink
            self.rPrice = rPrice
        
    rItemList = []
    rnsource = requests.get('https://rhensnesttoyshop.com/search?type=product&options%5Bprefix%5D=last&q={}'.format(term)).text
    rnsoup = BeautifulSoup(rnsource, "html.parser")
    testinfo = rnsoup.findAll("div", {"class":"product-block"})
    for t in testinfo:
        testsearch = t.findAll("img", {"class": "rimage__image"})
        n = str(testsearch).split("image\" src=\"")
        if len(n)>1:
            img = n[1].split("?v=")[0]
            name = t.find("a", {"class": "product-block__title-link"}).text
            link = t.find("a", {"product-block__title-link"})['href']
            price = t.find("span", {"class": "theme-money"}).text
            rItemList.append( rItem(img, name, link, price))
    # for obj in rItemList:
    #     print(obj.rImg)
    #     print(obj.rTitle)
    #     print(obj.rLink)
    #     print(obj.rPrice)

    # BRAVE + KIND
    class bkItem():
        def __init__(self, bkImg, bkTitle, bkLink, bkPrice):
            self.bkImg = bkImg
            self.bkTitle = bkTitle
            self.bkLink = bkLink
            self.bkPrice = bkPrice
        
    bkItemList = []
    bksource = requests.get('https://www.braveandkindbooks.com/search?q={}'.format(term)).text
    bksoup = BeautifulSoup(bksource, "html.parser")

    Html_file = open("raw.html", "w")
    Html_file.write(str(bksoup))
    Html_file.close()

    bkitemcard = bksoup.findAll("li", {"class": "list-view-item"})
    if len(bkitemcard) > 0:
        for item in bkitemcard:
            bkimage = item.find("img")
            if bkimage is None:
                continue
            else:
                bkimagesrc = bkimage['src']
                img = bkimagesrc.split("?v=")[0]
                name = item.find("div", {"class": "list-view-item__title"}).text
                link = item.find("a", {"class": "full-width-link"})['href']
                pricetest = item.find("span", {"class": "price-item--sale"})
                if pricetest is not None:
                    price = pricetest.text
                elif item.find("div", {"class": "list-view-item__sold-out"}) is not None:
                    price="Sold Out"
                else:
                    price=""
                bkItemList.append( bkItem(img, name, link, price))


    return render_template('results.html', term=term, thumbnails=thumbnails, 
            linx=linx, alts=alts, sites=sites,
            rItemList=rItemList, bkItemList=bkItemList
            )
