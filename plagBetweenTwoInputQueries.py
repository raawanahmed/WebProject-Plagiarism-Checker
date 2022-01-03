import math

from flask import request
from Constants import ERROR_NO_INPUT

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude, extractQueryText


def calcSimilarityBetweenTwoQueries():
    firstInputWords, firstInputWordsList = extractQueryText('query1')
    secondInputWords, secondInputWordsList = extractQueryText('query2')

    # check if data is present in both queries
    if firstInputWords == ERROR_NO_INPUT or secondInputWords == ERROR_NO_INPUT:
        return ERROR_NO_INPUT, ERROR_NO_INPUT, ERROR_NO_INPUT

    allWords = set()
    allWords = firstInputWords.union(secondInputWords)

    # TF frequency of word i in document j
    firstInputTfIdf = []
    secondInputTfIdf = []
    for word in allWords:
        cnt = 0
        if word in firstInputWordsList:
            cnt += 1
        if word in secondInputWordsList:
            cnt += 1
        idf = math.log(2*1.0/cnt*1.0)

        if idf == 0:
            idf = 1
        firstInputInputTfCounter = calcFrequency(
            word, firstInputWordsList) * idf
        secondInputTfCounter = calcFrequency(word, secondInputWordsList)*idf
        firstInputTfIdf.append(firstInputInputTfCounter)
        secondInputTfIdf.append(secondInputTfCounter)

    dotProduct = calcDotProduct(firstInputTfIdf, secondInputTfIdf)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(firstInputTfIdf))
    secondInputVectorMagnitude = math.sqrt(
        calcVectorMagnitude(secondInputTfIdf))
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * secondInputVectorMagnitude)) * 100

    percentageOfPlagiarism = "The two inputs match %0.02f%% with each other." % matchPercentage
    return percentageOfPlagiarism, request.form['query1'], request.form['query2']
