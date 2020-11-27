from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import sys

chItemList = []
def clubhouse(term):
    class chItem():
        def __init__(self, chImg, chTitle, chLink, chPrice):
            self.chImg = chImg
            self.chTitle = chTitle
            self.chLink = chLink
            self.chPrice = chPrice
    source = requests.get('https://www.clubhousekidandcraft.com/search?q={}'.format(term)).text
    soup = BeautifulSoup(source, "html.parser")
    thumbnails = soup.findAll("div", {"class": "grid"})
    chItemList.clear()
    if len(thumbnails) > 0:
        for t in thumbnails:
            imgs = t.find("div", {"class": "one-fifth"})
            # print(imgs)
            if imgs is not None:
                # print(imgs)
                imgtag = imgs.findAll("img")[1]
                img = "https:" + imgtag['src']
                name = t.find("a")['title']
                link = "https://www.clubhousekidandcraft.com" + t.find("a")['href']
                price = t.find("span", {"itemprop": "price"}).text.strip()
                chItemList.append( chItem(img, name, link, price))
        chItemList.pop(0)
    # Html_file = open("raw.html", "w")
    # Html_file.write(str(thumbnails))
    # Html_file.close()

# Rhens Nest
rItemList = []
def rhens(term):
    class rItem():
        def __init__(self, rImg, rTitle, rLink, rPrice):
            self.rImg = rImg
            self.rTitle = rTitle
            self.rLink = rLink
            self.rPrice = rPrice    
    rnsource = requests.get('https://rhensnesttoyshop.com/search?type=product&options%5Bprefix%5D=last&q={}'.format(term)).text
    rnsoup = BeautifulSoup(rnsource, "html.parser")
    testinfo = rnsoup.findAll("div", {"class":"product-block"})
    rItemList.clear()
    if len(testinfo) > 0:
        for t in testinfo:
            testsearch = t.findAll("img", {"class": "rimage__image"})
            n = str(testsearch).split("image\" src=\"")
            if len(n)>1:
                img = n[1].split("?v=")[0]
                name = t.find("a", {"class": "product-block__title-link"}).text
                link = t.find("a", {"product-block__title-link"})['href']
                price = t.find("span", {"class": "theme-money"}).text
                rItemList.append( rItem(img, name, link, price))

# Brave + Kind
bkItemList = []
def brave(term):
    class bkItem():
        def __init__(self, bkImg, bkTitle, bkLink, bkPrice):
            self.bkImg = bkImg
            self.bkTitle = bkTitle
            self.bkLink = bkLink
            self.bkPrice = bkPrice
    bksource = requests.get('https://www.braveandkindbooks.com/search?q={}'.format(term)).text
    bksoup = BeautifulSoup(bksource, "html.parser")
    bkitemcard = bksoup.findAll("li", {"class": "list-view-item"})
    bkItemList.clear()
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

# Baby Love
blItemList = []
def babyLove(term):
    class blItem():
            def __init__(self, blImg, blTitle, blLink, blPrice):
                self.blImg = blImg
                self.blTitle = blTitle
                self.blLink = blLink
                self.blPrice = blPrice
    blsource = requests.get('https://babyloveatlanta.com/search?q={}'.format(term)).text
    blsoup = BeautifulSoup(blsource, "html.parser")
    blitemcard = blsoup.findAll("div", {"class": "card"})
    blItemList.clear()
    if len(blitemcard) > 0:
        for item in blitemcard:
            blimage = item.findAll("img")[1]
            if blimage is None:
                continue
            else:
                blimagesrc = blimage['src']
                img = blimagesrc.split("?v=")[0]
                name = item.find("h3", {"class": "card__name"}).text
                link = item.find("a")['href']
                price = item.find("div", {"class": "card__price"}).text.strip()
                blItemList.append( blItem(img, name, link, price))

# Kazoo Toys
kzItemList = []
def kazoo(term):
    class kzItem():
        def __init__(self, kzImg, kzTitle, kzLink, kzPrice):
            self.kzImg = kzImg
            self.kzTitle = kzTitle
            self.kzLink = kzLink
            self.kzPrice = kzPrice
    kzsource = requests.get('https://kazootoysatlanta.com/?s={}&post_type=product&type_aws=true&aws_id=1&aws_filter=1'.format(term)).text
    kzsoup = BeautifulSoup(kzsource, "html.parser")
    kzitemcard = kzsoup.findAll("li", {"class": "product-type-simple"})
    kzItemList.clear()
    if len(kzitemcard) > 0:
        for item in kzitemcard:
            kzimage = item.findAll("img")[0]
            if kzimage is None:
                continue
            else:
                img = kzimage['src']
                name= item.find("h2", {"class": "woocommerce-loop-product__title"}).text
                link = item.find("a", {"class": "ast-loop-product__link"})['href']
                rawprice = item.find("bdi")
                price = str(rawprice).split("</span>")[1][:-6]
                kzItemList.append( kzItem(img, name, link, price))




def scrapeSites(term):
    # CLUBHOUSE INFO
    clubhouse(term)
    # RHEN'S NEST INFO
    rhens(term)
    # BRAVE + KIND
    brave(term)
    # Baby Love
    babyLove(term)
    # Kazoo Toys
    kazoo(term)