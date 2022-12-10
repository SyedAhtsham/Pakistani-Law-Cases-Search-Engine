import math

docIndexes = []
tf_idfs = []
vocabulary = dict()
queries = []
idfs = dict()



def L2NormOfVector(vector):
    result = 0
    total = 0
    for value in vector:
        total = total + (value * value)
    result = math.sqrt(total)
    return result

def countWordsInText(word, text):
    tokens = text.split(' ')
    count = 0
    for token in tokens:
        if token == word:
            count += 1
    return count

def getVocabularyId(voc):
    try:
        return vocabulary[voc]
    except:
        return '0'


def getTfIfdForDoc(vocId, docId):
    for item in tf_idfs:
        if item[0] == vocId:
            sep = item[1].split(' ')
            for item2 in sep:
                breakItem = item2.split(':')
                if breakItem[0] == docId:
                    return float(breakItem[1])
    return 0.0

def getNormalizedVector(vector):
    l2Norm = L2NormOfVector(vector)
    normalized = []
    if l2Norm > 0:
        for value in vector:
            val = float(value/l2Norm)
            normalized.append(val)
        return normalized
    return vector

def getTfIfdForQuery(word, query):
    tf = countWordsInText(word, query)
    logFreq = 0
    if tf > 0:
        logFreq = 1 + math.log10(tf)
    idf = 0
    vocId = getVocabularyId(word)
    if vocId != '0':
        idf = idfs[vocId]
    tfIdf = logFreq * idf
    return round(tfIdf, 3)

def computeDotProduct(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result


# Read document indexes
file = open('documentIndex.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    docIndexes.append(sep)
file.close()

# Read tf_idfs
file = open('tf_idf.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split('\t')
    tf_idfs.append(sep)
file.close()

# Read vocabulary
file = open('sortedVocabularyWithNames.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    vocabulary[sep[1]] = sep[0]
file.close()
# Read queries from file
file = open('queries(tf_ifdf).txt', 'r')
for line in file:
    data = line.strip('\n')
    queries.append(data)
file.close()

# Read idfs
file = open('idf.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    idfs[sep[0]] = float(sep[1])

file.close()
queryIdx = 2

file2 = open('cosineScores(tf_idf).txt', 'w')




for query in queries:

    docNames = []
    scores = []

    query.lower()
    queryTokens = query.split(' ')

    file2.write(query + '\n')
    file2.write('Weighting Scheme: TFIDF' + '\n')

    # Read tokens for each document
    for item in docIndexes:

        wordsSet = set()
        docScoreVector = []
        docNormalizedVector = []
        queryScoreVector = []
        queryNormalizedVector = []


        docId = item[0]
        docName = 'File cases tokens\\' + item[1] + '.txt'
        file = open(docName, 'r')
        for line in file:
            token = line.strip('\n')
            if token in queryTokens:
                wordsSet.add(token)

        # Document Part
        for word in wordsSet:
            tf_idf = 0
            vocId = getVocabularyId(word)
            if vocId != '0':
                tf_idf = getTfIfdForDoc(vocId, docId)
            docScoreVector.append(float(tf_idf))



        # Query Part
        for word in wordsSet:
            tf_idf = getTfIfdForQuery(word, query)
            queryScoreVector.append(tf_idf)


        if len(docScoreVector) > 0 and len(queryScoreVector) > 0:
            docNormalizedVector = getNormalizedVector(docScoreVector)
            queryNormalizedVector = getNormalizedVector(queryScoreVector)

        cosineScore = 0.0

        if len(queryNormalizedVector) > 0 and len(docNormalizedVector) > 0:
            cosineScore = computeDotProduct(docNormalizedVector, queryNormalizedVector)

        if cosineScore > 0:
            scores.append(round(cosineScore, 3))
            docNames.append(docName)

    if len(scores) > 0:
        for i in range(len(scores)-1):
            for j in range(len(scores)-i-1):
                if scores[j] < scores[j+1]:
                    temp = scores[j]
                    scores[j] = scores[j+1]
                    scores[j+1] = temp
                    temp = docNames[j]
                    docNames[j] = docNames[j+1]
                    docNames[j+1] = temp

        i = 0
        while i < len(scores) and i < 10:
            file2.write(docNames[i] + ' ' + str(scores[i]) + '\n')
            i += 1

    else:
        file2.write('No Documents Found\n')

    file2.write('\n')

file2.close()
print('\n > All data is saved into text file ...')