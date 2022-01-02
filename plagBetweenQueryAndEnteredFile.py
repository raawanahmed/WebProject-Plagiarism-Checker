import math
import os
import re
from helperFunctions import calcDotProduct, calcFrequency, calcVectorMagnitude
from flask import request




def calcSimilarity2():
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
    # load all the path ".cpp" files on project directory.
    curDatabase = open(files[0], encoding="utf-8").read().lower()
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


def deleteTxtFiles():
    files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    if len(files) > 0:
        for f in files:
            os.remove(f)
# directory = "./database"
# files_in_directory = os.listdir(directory)
# filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
# if len(filtered_files) > 0:
#    for file in filtered_files:
#       path_to_file = os.path.join(directory, file)
# os.remove(path_to_file)
