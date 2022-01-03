import math

from flask import request
from Constants import ERROR_NO_INPUT

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude, extractQueryText

def calcSimilarityBetweenTwoQueries():
    firstInputWords, firstInputWordsList = extractQueryText('query1')
    secondInputWords, secondInputWordsList = extractQueryText('query2')

    #check if data is present in both queries 
    if firstInputWords == -1 or secondInputWords == -1:
        return ERROR_NO_INPUT


    allWords = set()
    allWords = firstInputWords.union(secondInputWords)

    # TF frequency of word i in document j
    firstInputTF = []
    secondInputTF = []
    for word in allWords:
        cnt = 0
        firstInputInputTfCounter = calcFrequency(word, firstInputWordsList)
        if word in firstInputWordsList:
            cnt += 1
        if word in secondInputWordsList:
            cnt += 1
        idf = math.log10(2*1.0/cnt*1.0)

        if idf == 0:
            idf = 1
        secondInputTFCounter = calcFrequency(word, secondInputWordsList)*idf
        firstInputTF.append(firstInputInputTfCounter)
        secondInputTF.append(secondInputTFCounter)

    dotProduct = calcDotProduct(firstInputTF, secondInputTF)
    queryVectorMagnitude = math.sqrt(calcVectorMagnitude(firstInputTF))
    secondInputVectorMagnitude = math.sqrt(calcVectorMagnitude(secondInputTF))
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * secondInputVectorMagnitude)) * 100

    percentage = "The two queries match %0.02f%% with each other." % matchPercentage
    return percentage, request.form['query1'], request.form['query2']
