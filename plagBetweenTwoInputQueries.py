import math
import re

from flask import request

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude


def extractQueryText(HtmlElementName):
    allWords = set()
    inputQuery = request.form[HtmlElementName]
    inputQuery = inputQuery.lower()
    # Replace punctuation by space and split
    inputWordsList = re.sub("[^\w]", " ", inputQuery).split()
    if len(inputWordsList) == 0:
        return -1, -1
    for word in inputWordsList:
        allWords.add(word)
    return allWords, inputWordsList
    # allWords -> is a set contains all words in inputQuery
    # inputWordsList ->  this is the input query after filtering it from punctuations


def calcSimilarityBetweenTwoQueries():
    firstInputWords, firstInputWordsList = extractQueryText('query1')
    secondInputWords, secondInputWordsList = extractQueryText('query2')
    if firstInputWords == -1 or secondInputWords == -1:
        return -1
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
        print("////////", idf)
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
    percentageOfPlagiarism = dict()
    percentageOfPlagiarism['inputQuery1'] = request.form['query1']
    percentageOfPlagiarism['inputQuery2'] = request.form['query2']
    percentageOfPlagiarism['output'] = percentage
    return percentageOfPlagiarism
