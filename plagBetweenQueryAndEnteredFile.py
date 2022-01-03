import math
import os
import re
from helperFunctions import extractQueryText
from flask import request
from Constants import ERROR_NO_FILES, ERROR_NO_INPUT

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude


def calcSimilarityBetweenQueryAndFile():
    # allWords is a "set" that will store each word in both the file and the text
    allWords, queryWordsList  = extractQueryText('query')

    files = [doc for doc in os.listdir() if doc.endswith('.txt')] 
    # check that the user enetered text and uploaded a file 
    if len(files) == 0:
        return ERROR_NO_FILES
    if len(queryWordsList) == 0:
        return ERROR_NO_INPUT

    curFile = open(files[0], encoding="utf-8").read().lower() # read the file and convert all its words to lowercase letters
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

    percentageOfPlagiarism = "Input query text matches %0.02f%% with database." % matchPercentage
   
    return percentageOfPlagiarism
