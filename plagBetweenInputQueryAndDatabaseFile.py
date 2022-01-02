import math
import os
import re

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

    inputQuery = request.form['query1']
    lowercaseQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", lowercaseQuery).split()
    if len(queryWordsList) == 0:
        return 0
    for word in queryWordsList:
        allWords.add(word)

    # path_to_file = os.path.join("./database", "team.txt")
    curDatabase = request.form['query2']
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
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    output = "The two queries matches %0.02f%% with each other." % matchPercentage
    d = dict()
    d['inputQuery'] = inputQuery
    d['output'] = output
    return d
