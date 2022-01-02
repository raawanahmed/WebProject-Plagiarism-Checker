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