import math
import os
import re

from flask import request

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude


def calcSimilarityBetweenQueryAndFile():
    allWords = set()
    inputQuery = request.form['query']
    lowercaseQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", lowercaseQuery).split()
    for word in queryWordsList:
        allWords.add(word)

    files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    if len(files) == 0:
        return 0
    if len(queryWordsList) == 0:
        return -1

    curFile = open(files[0], encoding="utf-8").read().lower()
    # Replace punctuation by space and split
    fileWordsList = re.sub("[^\w]", " ", curFile).split()
    for word in fileWordsList:
        allWords.add(word)

    # TF frequency of word i in document j
    inputQueryTF = []
    databaseTF = []
    for word in allWords:
        queryTfCounter = calcFrequency(word, queryWordsList)
        databaseTfCounter = calcFrequency(word, fileWordsList)
        inputQueryTF.append(queryTfCounter)
        databaseTF.append(databaseTfCounter)

    dotProduct = calcDotProduct(inputQueryTF, databaseTF)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(inputQueryTF))
    databaseVectorMagnitude = math.sqrt(calcVectorMagnitude(databaseTF))
    matchPercentage = float(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    percentages = "Input query text matches %0.02f%% with database." % matchPercentage
    percentageOfPlagiarism = dict()
    percentageOfPlagiarism['output'] = percentages
    return percentageOfPlagiarism
