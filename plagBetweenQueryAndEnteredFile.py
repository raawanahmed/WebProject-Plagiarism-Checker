import math
import os
import re
from helperFunctions import extractQueryText
from flask import request
from Constants import ERROR_EMPTY_FILE, ERROR_NO_FILES, ERROR_NO_INPUT

from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude


def calcSimilarityBetweenQueryAndFile():
    # allWords is a "set" that will store each word in both the file and the text
    allWords, queryWordsList = extractQueryText('query')

    files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    # check that the user enetered text and uploaded a file
    if len(files) == 0:
        return ERROR_NO_FILES
    if allWords == ERROR_NO_INPUT or queryWordsList == ERROR_NO_INPUT:
        return ERROR_NO_INPUT
    if len(queryWordsList) == 0:
        return ERROR_NO_INPUT

    # read the file and convert all its words to lowercase letters
    curFile = open(files[0], encoding="utf-8").read().lower()
    if len(curFile) == 0:
        return ERROR_EMPTY_FILE
    # Replace punctuation by space and split
    fileWordsList = re.sub("[^\w]", " ", curFile).split()

    for word in fileWordsList:
        allWords.add(word)

    # TF frequency of word i in document j
    TfIdfOfWordsInInputText = []
    TfidfOfWordsInFile = []
    for word in allWords:
        cnt = 0
        if word in queryWordsList:
            cnt += 1
        if word in fileWordsList:
            cnt += 1
        idf = math.log(2*1.0/cnt*1.0)
        if idf == 0:
            idf = 1
        counterOfWordInInputTextWithIdf = calcFrequency(
            word, queryWordsList)*idf
        counterOfWordInFileWithIdf = calcFrequency(word, fileWordsList)*idf
        TfIdfOfWordsInInputText.append(counterOfWordInInputTextWithIdf)
        TfidfOfWordsInFile.append(counterOfWordInFileWithIdf)

    dotProduct = calcDotProduct(TfIdfOfWordsInInputText, TfidfOfWordsInFile)
    queryVectorMagnitude = math.sqrt(
        calcVectorMagnitude(TfIdfOfWordsInInputText))
    databaseVectorMagnitude = math.sqrt(
        calcVectorMagnitude(TfidfOfWordsInFile))
    matchPercentage = float(
        dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    percentageOfPlagiarism = "Input query text matches %0.02f%% with database." % matchPercentage

    return percentageOfPlagiarism
