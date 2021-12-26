import re
import math
from flask import request


def calcFrequency(word, wordsList):
    freq = 0
    for w in wordsList:
        if word == w:
            freq += 1
    return freq


def calcVectorMagnitude(TFarray):
    vectorMagnitude = 0
    for i in range(len(TFarray)):
        vectorMagnitude += TFarray[i] ** 2
    return vectorMagnitude


def calcDotProduct(inputQueryTF, databaseTF):
    dotProduct = 0
    for i in range(len(inputQueryTF)):
        dotProduct += inputQueryTF[i] * databaseTF[i]
    return dotProduct


def calcSimilarity():
    allWords = set()

    inputQuery = request.form['query']
    lowercaseQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", lowercaseQuery).split()
    for word in queryWordsList:
        allWords.add(word)

    curDatabase = open("database1.txt", "r").read().lower()
    # Replace punctuation by space and split
    databaseWordsList = re.sub("[^\w]", " ", curDatabase).split()
    for word in databaseWordsList:
        allWords.add(word)

    # TF frequency of word i in document j
    inputQueryTF = []
    databaseTF = []
    for word in allWords:
        queryTfCounter = calcFrequency(word, queryWordsList)
        databaseTfCounter = calcFrequency(word, databaseWordsList)
        inputQueryTF.append(queryTfCounter)
        databaseTF.append(databaseTfCounter)

    dotProduct = calcDotProduct(inputQueryTF, databaseTF)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(inputQueryTF))
    databaseVectorMagnitude = math.sqrt(calcVectorMagnitude(databaseTF))
    matchPercentage = float(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    output = "Input query text matches %0.02f%% with database." % matchPercentage
    d = dict()
    d['inputQuery'] = inputQuery
    d['output'] = output
    return d
