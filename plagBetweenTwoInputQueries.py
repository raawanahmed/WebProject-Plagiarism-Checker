import math
import re

from flask import request

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude


def extractQueryText(HtmlElementName):
    allWords = set()
    inputQuery = request.form[HtmlElementName]
    inputQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", inputQuery).split()
    if len(queryWordsList) == 0:
        return -1, -1
    for word in queryWordsList:
        allWords.add(word)
    return allWords, queryWordsList
    # allWords -> is a set contains all words in inputQuery
    # QueryWordsList ->  this is the input query after filtering it from punctuations


def calcSimilarityBetweenTwoQueries():
    firstQueryWords, firstQueryWordsList = extractQueryText('query1')
    secondQueryWords, secondQueryWordList = extractQueryText('query2')
    if firstQueryWords == -1 or secondQueryWords == -1:
        return -1
    allWords = set()
    allWords = firstQueryWords.union(secondQueryWords)

    # TF frequency of word i in document j
    firstInputQueryTF = []
    secondInputQueryTF = []
    for word in allWords:
        firstInputQueryTfCounter = calcFrequency(word, firstQueryWordsList)
        secondInputQueryTFCounter = calcFrequency(word, secondQueryWordList)
        firstInputQueryTF.append(firstInputQueryTfCounter)
        secondInputQueryTF.append(secondInputQueryTFCounter)

    dotProduct = calcDotProduct(firstInputQueryTF, secondInputQueryTF)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(firstInputQueryTF))
    databaseVectorMagnitude = math.sqrt(calcVectorMagnitude(secondInputQueryTF))
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    percentage = "The two queries match %0.02f%% with each other." % matchPercentage
    percentageOfPlagiarism = dict()
    percentageOfPlagiarism['inputQuery1'] = request.form['query1']
    percentageOfPlagiarism['inputQuery2'] = request.form['query2']
    percentageOfPlagiarism['output'] = percentage
    return percentageOfPlagiarism
