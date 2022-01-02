import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# files = []
# for file in os.listdir():
#    if file.endswith('.txt'):
#        files.append(file)

plagiarismResults = set()


def vectorize(Data):
    return TfidfVectorizer().fit_transform(Data).toarray()


# cosine similarity to compute the Plagiarism.
def similarity(code_1, code_2):
    return cosine_similarity([code_1, code_2])


def cosineSimilarity(x, y):
    # Ensure length of x and y are the same
    # if len(x) != len(y):
    #   return None
    dot_product = np.dot(x, y)
    magnitude_x = np.sqrt(np.sum(x ** 2))
    magnitude_y = np.sqrt(np.sum(y ** 2))
    cos_similarity = dot_product / (magnitude_x * magnitude_y)
    return cos_similarity


def PlagiarismChecker(filesWithTheirVectors):
    for curFile, curVector in filesWithTheirVectors:
        temp = filesWithTheirVectors.copy()
        current_index = temp.index((curFile, curVector))
        del temp[current_index]
        for otherFile, otherVector in temp:
            scoreOfSimilarity = cosineSimilarity(curVector, otherVector)
            file_pair = sorted((curFile, otherFile))
            score = (file_pair[0], file_pair[1], "{:.2%}".format(scoreOfSimilarity))
            plagiarismResults.add(score)
    return plagiarismResults


def solve():
    # Reading all ".txt" files
    files = [doc for doc in os.listdir() if doc.endswith('.txt')]

    if len(files) == 0:
        return -1
    # load all the path ".txt" files on project directory.
    fileStore = [open(_file, encoding="utf-8").read() for _file in files]
    # Vectorize the data.
    # The zip() function takes iterables (can be zero or more), aggregates them in a tuple, and returns it.
    vectors = vectorize(fileStore)
    filesWithTheirVectors = list(zip(files, vectors))
    return PlagiarismChecker(filesWithTheirVectors)


def deleteFiles():
    files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    if len(files) > 0:
        for f in files:
            os.remove(f)
