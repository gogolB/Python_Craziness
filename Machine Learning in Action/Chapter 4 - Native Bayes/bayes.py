from numpy import *

# Loads a testing Dataset.
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']];
    # 1 is abusive, 0 not.
    classVec = [0,1,0,1,0,1];
    return postingList,classVec;

# Creates a list of words from the given dataset so that each word does not
# appear more than once in the given dataset.
def createVocabList(dataSet):
    vocabSet = set([]);
    for document in dataSet:
        vocabSet = vocabSet | set(document);
    return list(vocabSet);

# Turns a set of words in to a vector.
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList);
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1;
        else:
            print ("the word: %s is not in my Vocabulary!" % (word));
    return returnVec

# Trains the native Bayes ML system.
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix);
    numWords = len(trainMatrix[0]);
    pAbusive = sum(trainCategory)/float(numTrainDocs);
    p0Num = ones(numWords); p1Num = ones(numWords);
    p0Denom = 2.0;
    p1Denom = 2.0;

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i];
            p1Denom += sum(trainMatrix[i]);
        else:
            p0Num += trainMatrix[i];
            p0Denom += sum(trainMatrix[i]);
    p1Vect = log(p1Num/p1Denom);
    p0Vect = log(p0Num/p0Denom);
    return p0Vect,p1Vect,pAbusive;

# Classifies something once the native Bayes ML systems has been trained.
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1);                              # Element-wise mult.
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1);
    if p1 > p0:
        return 1;
    else:
        return 0;

# Creates a bag of words. (NOT A SET!)
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList);
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1;
    return returnVec;

# Function to test the Native Bayes systems.
def testingNB():
    listOPosts,listClasses = loadDataSet();
    myVocabList = createVocabList(listOPosts);
    trainMat=[];
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc));
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses));
    testEntry = ['love', 'my', 'dalmation'];
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry));
    print (testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb));
    testEntry = ['stupid', 'garbage'];
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry));
    print (testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb));

# Parses a bigstring and returns a list of words.
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString);
    return [tok.lower() for tok in listOfTokens if len(tok) > 2];

# Unit test for the spam system.
def spamTest():
    docList=[];
    classList = [];
    fullText =[];

    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read());
        docList.append(wordList);
        fullText.extend(wordList);
        classList.append(1);
        wordList = textParse(open('email/ham/%d.txt' % i).read());
        docList.append(wordList);
        fullText.extend(wordList);
        classList.append(0);
    # Create vocabulary
    vocabList = createVocabList(docList);
    trainingSet = list(range(50));
    testSet=[];
    # Create test set
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)));
        testSet.append(trainingSet[randIndex]);
        del(trainingSet[randIndex]);
    trainMat=[];
    trainClasses = [];

    # Train the classifier.
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]));
        trainClasses.append(classList[docIndex]);
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses));
    errorCount = 0;

    # Classify the remaining.
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex]);
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1;
            print ("classification error",docList[docIndex]);
    print ('the error rate is: ',float(errorCount)/len(testSet));
    #return vocabList,fullText

# Gets the most frequent words.
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}

    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

# Figure out the local words in an area, these are the most commonly used words
# Should find a way to ignore stop words.
# Requires feedparser which can be found at: https://github.com/kurtmckee/feedparser
def localWords(feed1,feed0):
    import feedparser
    docList=[];
    classList = [];
    fullText =[]
    minLen = min(len(feed1['entries']),len(feed0['entries']));

    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary']);
        docList.append(wordList);
        fullText.extend(wordList);
        classList.append(1);
        wordList = textParse(feed0['entries'][i]['summary']);
        docList.append(wordList);
        fullText.extend(wordList);
        classList.append(0);
    vocabList = createVocabList(docList);
    top30Words = calcMostFreq(vocabList,fullText);

    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0]);
    trainingSet = list(range(2*minLen));
    testSet=[];

    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)));
        testSet.append(trainingSet[randIndex]);
        del(trainingSet[randIndex]);
    trainMat=[];
    trainClasses = [];

    # Train the classifier.
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]));
        trainClasses.append(classList[docIndex]);
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses));
    errorCount = 0;

     # Classify the remaining.
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex]);
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1;
    print ('the error rate is: ',float(errorCount)/len(testSet));
    return vocabList,p0V,p1V;

# Gets the top words in SF and NY.
def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf);
    topNY=[];
    topSF=[];
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]));
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]));
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True);
    print ("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**");
    for item in sortedSF:
        print (item[0]);
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True);
    print ("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**");
    for item in sortedNY:
        print (item[0]);

# Craigslist example from the book.
# Requires feedparser which can be found at: https://github.com/kurtmckee/feedparser
def craigslistFeedTest():
    import feedparser;
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss');
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss');
    localWords(ny, sf);
    getTopWords(ny, sf);
