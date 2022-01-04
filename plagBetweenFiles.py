import os

from sklearn.feature_extraction.text import TfidfVectorizer
from Constants import ERROR_EMPTY_FILE, ERROR_NO_FILES, ERROR_ONE_FILE_ONLY

from helperFunctions import extractFiles, cosineSimilarity


plagiarismResults = set()


def PlagiarismChecker(filesWithTheirVectors):
    #curVector -> list of weights of current file

    for curFile, curVector in filesWithTheirVectors:
        temp = filesWithTheirVectors.copy()
        current_index = temp.index((curFile, curVector))
        del temp[current_index]
        for otherFile, otherVector in temp:
            scoreOfSimilarity = cosineSimilarity(curVector, otherVector) 
            file_pair = sorted((curFile, otherFile))
            score = (file_pair[0], file_pair[1],
                     "{:.2%}".format(scoreOfSimilarity))         
            plagiarismResults.add(score)
    return sorted(plagiarismResults)


# return nd-array [[tf*idf for each txt file], etc]
def vectorize(Data):
    return TfidfVectorizer().fit_transform(Data).toarray()


def calcSimilarityBetweenFiles():
    # load all the path ".txt" files on files directory.
    directory = os.getcwd() + "/files"
    nameOfEachFile, pathOfFiles = extractFiles(directory)
    # check if there is files in directory
    if len(pathOfFiles) == 0:
        return ERROR_NO_FILES
    if len(pathOfFiles) == 1:
        return ERROR_ONE_FILE_ONLY
    # open all files in pathOfFiles, file of store will contain list every index is list of strings in each file 
    # fileStore=[["hi", "there"], ["", ""], ["", ""]]   
    fileStore = [open(file, encoding="utf-8").read().lower()
                 for file in pathOfFiles]
    for fileData in fileStore:
        if len(fileData) == 0:
            return ERROR_EMPTY_FILE
    # Vectorize the data.
    vectors = vectorize(fileStore)
    # The zip() function takes iterables (can be zero or more), aggregates them in a tuple, and returns it.
    filesWithTheirVectors = list(zip(nameOfEachFile, vectors)) #["nameOFFile.txt", [.1, .5, ..weights of every word] ] 
    return PlagiarismChecker(filesWithTheirVectors)
