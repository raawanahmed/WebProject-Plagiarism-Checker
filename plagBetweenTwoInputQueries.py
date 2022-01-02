import math
import os
import re
from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude
from flask import request


def extractQueryText(HtmlElementName):
    allWords = set()
    inputQuery = request.form[HtmlElementName]
    inputQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", inputQuery).split()
    if len(queryWordsList) == 0:
        return -1
    for word in queryWordsList:
        allWords.add(word)
    return allWords, queryWordsList
     # allWords -> is a set contains all words in inputQuery 
     #  QueryWordsList ->  this is the input query after filtering it from punctuations

def calcSimilarity():
    allWords = set()
    fisrtQueryWords, firstQueryWordsList = extractQueryText('query1')
    secondQueryWords, seondQueryWordList = extractQueryText('query2')

    allWords = fisrtQueryWords.union(secondQueryWords)
    
    
    # TF frequency of word i in document j
    inputQueryTF = []
    secondInputQueryTF = []
    for word in allWords:
        queryTfCounter = calcFrequency(word, firstQueryWordsList)
        secondInputQueryTFCounter = calcFrequency(word, seondQueryWordList)
        inputQueryTF.append(queryTfCounter)
        secondInputQueryTF.append(secondInputQueryTFCounter)

    dotProduct = calcDotProduct(inputQueryTF, secondInputQueryTF)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(inputQueryTF))
    databaseVectorMagnitude = math.sqrt(calcVectorMagnitude(secondInputQueryTF))
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    output = "The two queries match %0.02f%% with each other." % matchPercentage
    d = dict()
    d['inputQuery1'] = request.form['query1']
    d['inputQuery2'] = request.form['query2']
    d['output'] = output
    return d
