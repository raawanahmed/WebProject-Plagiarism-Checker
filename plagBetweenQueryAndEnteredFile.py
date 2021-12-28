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
    inputQuery = request.form['query']
    lowercaseQuery = inputQuery.lower()
    # Replace punctuation by space and split
    queryWordsList = re.sub("[^\w]", " ", lowercaseQuery).split()
    for word in queryWordsList:
        allWords.add(word)

    file = os.listdir("./database/")
    curDatabase = open(file[0], encoding="utf-8").read().lower()
    # Replace punctuation by space and split
    fileWordsList = re.sub("[^\w]", " ", curDatabase).split()
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

    output = "Input query text matches %0.02f%% with database." % matchPercentage
    d = dict()
    d['inputQuery'] = inputQuery
    d['output'] = output
    return d


def deleteFileInDatabaseFolder():
    directory = "./database"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

