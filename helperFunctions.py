from flask import request, render_template
import re
import os
import numpy as np


def calcFrequency(word, wordsList):
    freq = 0
    for curWord in wordsList:
        if word == curWord:
            freq += 1
    return freq


def calcVectorMagnitude(TFarray):
    vectorMagnitude = 0
    for idx in range(len(TFarray)):
        vectorMagnitude += TFarray[idx] ** 2
    return vectorMagnitude


def calcDotProduct(listOfText1, listOfText2):
    return np.dot(listOfText1, listOfText2)


def extractFiles(filesPath: str):
    txtFiles = [file for file in os.listdir(filesPath) if
                file.endswith(".txt")]  # list of file names in files directory
    pathOfFiles = set()
    nameOfEachFile = set()
    for i in range(len(txtFiles)):
        pathOfFiles.add(filesPath + "/" + txtFiles[int(i)])
        nameOfEachFile.add(txtFiles[int(i)])
    return nameOfEachFile, pathOfFiles


def extractQueryText(htmlElementName: str):
    # extract text entered by user given the htmlElementName

    allWords = set()
    inputQuery = request.form[htmlElementName]
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


def clearAllExistingFiles():
    # delete files that have been uploaded when comparing multiple files
    deleteUserInputFiles()
    # delete files that have been uploaded when comparing input text with a file
    deleteTxtFiles()


def renderPage(fileName="", query="", query1="", query2="", output="", warningMessage="", greetingMessage="", results=""):
    # clear all input files is there were any, then render the html page
    clearAllExistingFiles()
    return render_template(fileName, query=query, query1=query1, query2=query2, output=output,
                           warningMessage=warningMessage, greetingMessage=greetingMessage, results=results)


def deleteTxtFiles():
    files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    # check if there is files in directory
    if len(files) > 0:
        for file in files:
            os.remove(file)


def deleteUserInputFiles():
    # delete all files that the user may have input while checking
    # for plagiarism if they exist
    directory = "./files"
    if not os.path.exists(directory):
        return

    files_in_directory = os.listdir(directory)
    filtered_files = [
        file for file in files_in_directory if file.endswith(".txt")]
    if len(filtered_files) > 0:
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)


def cosineSimilarity(listOfWords1, listOfWords2):
    dot_product = calcDotProduct(listOfWords1, listOfWords2)
    magnitudeOfListOfWords1 = np.sqrt(np.sum(listOfWords1 ** 2))
    magnitudeOfListOfWords2 = np.sqrt(np.sum(listOfWords2 ** 2))
    cos_similarity = dot_product / (magnitudeOfListOfWords1 * magnitudeOfListOfWords2)
    return cos_similarity
