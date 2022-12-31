from bs4 import BeautifulSoup
import requests
import time
import datetime
from functools import reduce
import smtplib
import re
import csv
import uuid

path = "./cities.csv"
rootPath = "tempCSVFiles/"


def remove(string):
    return reduce(lambda x, y: (x+y) if (y != " " and y != "\n") else x, string, "")


def processElement(ele):
    if (ele is None or type(ele) == 'NoneType'):
        return "None"
    return ele.getText()


def getSoupFromTag(soup, _id=None, _class=None):
    if (_id == None and _class == None):
        return None
    if (_id != None):
        return soup.find(id=_id)
    return soup.select_one(_class)


def createSoup(page):
    soup_temp = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup_temp.prettify(), "html.parser")
    return soup


def createCSVFileFromDict(dictItem):
    fileName = str(uuid.uuid4()) + ".csv"
    with open(rootPath + str(fileName), 'w') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, dictItem.keys())
        w.writeheader()
        w.writerow(dictItem)

    return fileName


def createCSVFileFromDictList(dictList):
    fileName = str(uuid.uuid4()) + ".csv"
    with open(str(rootPath + fileName), 'w') as f:
        for dictItem in dictList:
            w = csv.DictWriter(f, dictItem.keys())
            w.writeheader()
            w.writerow(dictItem)
    return fileName


def getInfo(soup, x):

    productDict = dict()
    # print('data-index', )
    productDict['data-index'] = '{}'.format(x)
    individual_item = soup.find(
        'div', attrs={'data-index': '{}'.format(x)})  # x = 3
    if (individual_item == 'None'):
        return
    individual_item_price = remove(processElement(
        individual_item.find('span', attrs={"class": "a-price-whole"})).strip())
    # print(individual_item_price)
    productDict['individual_item_price'] = individual_item_price
    individual_item_rating = processElement(individual_item.find(
        'span', attrs={"class": "a-icon-alt"})).strip()

    productDict['individual_item_rating'] = individual_item_rating
    # print(individual_item_rating)
    individual_item_original_price = processElement(
        individual_item.find('span', attrs={"class": "a-offscreen"})).strip()

    productDict['individual_item_original_price'] = individual_item_original_price
    # print(individual_item_original_price)
    individual_item_img = individual_item.find('img')
    if (individual_item_img is not None):
        productDict['Title'] = individual_item_img['alt']
        productDict['imageURL'] = individual_item_img['src']
        # print("Title: ", individual_item_img['alt'])
        # print("imageURL: ", individual_item_img['src'])
    else:
        productDict['Title'] = "None"
        productDict['imageURL'] = "None"
        # print("Title: ", "None")
        # print("imageURL: ", "None")
    return productDict


def getInfo1Mg(item):
    productDict = dict()
    productDict["Title"] = "None"
    productDict["Quantity"] = "None"
    productDict["Price"] = "None"
    productDict["Rating"] = "None"
    productDict["TotalRating"] = "None"

    productDict["Title"] = (processElement(
        item.find(class_=re.compile(r'^style__pro-title'))).strip())
    productDict["Quantity"] = (processElement(
        item.find(class_=re.compile(r'^style__pack-size'))).strip())
    productDict["Price"] = (remove(processElement(
        item.find(class_=re.compile(r'^style__price-tag')))))
    productDict["Rating"] = (processElement(
        item.find(class_=re.compile(r'^CardRatingDetail__w'))).strip())
    productDict["TotalRating"] = (processElement(item.find(class_=re.compile(
        r'^CardRatingDetail__ratings-header'))).strip())

    return productDict


def getSingleProductDetailFromAmazon(url, headers):
    page = requests.get(url, headers=headers)
    soup = createSoup(page)
    print(soup)
    productDict = dict()
    productDict['title'] = processElement(getSoupFromTag(soup=soup, _id='productTitle')).strip()
    productDict['price'] = remove(processElement(getSoupFromTag(soup, _class='.a-price-whole')).strip())
    productDict['original_price'] = remove(processElement(getSoupFromTag(soup, _class='.a-price-whole')).strip())
    # precent_discount = remove(soup.select_one('.savingsPercentage').getText().strip())
    # product_details = soup.find(id='detailBullets_feature_div').select('li')
    # for product in product_details:
    # temp = remove(product.getText().strip()).split(":")
    # productDict[temp[0]] = temp[1]
    # product_details = soup.find(id='quickPromoBucketContent').select('li')
    # for product in product_details:
    # promo = remove(product.getText().strip())
    # productDict[promo] = promo

    productDict['merchant-info'] = remove(processElement(soup.find(id='merchant-info')).strip())
    productDict['availability'] = remove(processElement(soup.find(id='availability')).strip())
    return createCSVFileFromDict(productDict)


def getSearchQueryResult(url, headers, indexLimit):
    page = requests.get(url, headers=headers)
    soup = createSoup(page)
    productList = list()
    for x in range(0, indexLimit):
        productList.append(getInfo(soup, x))
    return createCSVFileFromDictList(productList)


def getSearchQueryResultFrom1Mg(url, headers):
    print("hiii")
    print(url)
    page = requests.get(url, headers=headers)
    soup = createSoup(page)
    product_items = soup.find('div', attrs={'class': 'product-card-container'})
    # print(product_items)

    product_items_list = soup.find_all(
        class_=re.compile(r'^style__product-box'))

    productList = list()
    for item in product_items_list:
        productList.append(getInfo1Mg(item))

    print(productList)
    return createCSVFileFromDictList(productList)

def getInfo1MgSingle(item):
    productDict = dict()
    productDict["Title"] = "None"
    productDict["Quantity"] = "None"
    productDict["Price"] = "None"
    productDict["Rating"] = "None"
    productDict["TotalRating"] = "None"

    productDict["Title"] = (processElement(
        item.find(class_=re.compile(r'^ProductTitle__product-title'))).strip())
    productDict["Quantity"] = (processElement(
        item.find(class_=re.compile(r'^OtcVariantsItem__variant-text'))).strip())
    productDict["Price"] = (remove(processElement(
        item.find(class_=re.compile(r'^PriceBoxPlanOption__offer-price')))))
    productDict["Rating"] = (processElement(
        item.find(class_=re.compile(r'^RatingDisplay__ratings-container'))).strip())
    productDict["TotalRating"] = (processElement(item.find(class_=re.compile(
        r'^RatingDisplay__ratings-header'))).strip())
    productDict["Description"] = (remove(processElement(item.find(class_=re.compile(
        r'^ProductDescription__product-description'))).strip()))
    return productDict

def getSingleResultFrom1Mg(url,headers):
    page = requests.get(url, headers=headers)
    soup = createSoup(page)
    product_item = soup.find('div',attrs={'class':'otc-container'})
    return createCSVFileFromDict(getInfo1MgSingle(product_item))
    
