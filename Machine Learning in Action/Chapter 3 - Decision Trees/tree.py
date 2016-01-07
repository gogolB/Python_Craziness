from math import log
import operator

# Function to calculate the Shannon entropy of a dataset.
def calcShannonEnt(dataset):
    numEntries = len(dataset);
    labelCounts= {};
    for featVec in dataset:
        currentLabel = featVec[-1];
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0;
        labelCounts[currentLabel] += 1;

    shannonEnt = 0.0;
    for key in labelCounts.keys():
        prob = float(labelCounts[key])/numEntries;
        shannonEnt -= prob * log(prob,2);

    return shannonEnt;

# Function to create a test Dataset.
def createDataSet():
    dataset = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']];
    labels = ['no surface', 'flippers'];

    return dataset, labels;

# Dataset splitting on a given value
def splitDataSet(dataSet, axis, value):
    retDataSet = [];
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis];
            reducedFeatVec.extend(featVec[axis+1:]);
            retDataSet.append(reducedFeatVec);
    return retDataSet;

# Chooseing the best feature to split on.
def chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0]) - 1;
    baseEntropy = calcShannonEnt(dataset);
    bestInfoGain = 0.0; bestFeature = -1;
    for i in range(numFeatures):
        featList = [example[i] for example in dataset];
        uniqueVals = set(featList);
        newEntropy = 0.0;
        for value in uniqueVals:
            subDataSet = splitDataSet(dataset, i, value);
            prob = len(subDataSet)/float(len(dataset));
            newEntropy += prob * calcShannonEnt(subDataSet);
        infoGain = baseEntropy - newEntropy;
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain;
            bestFeature = i;
        return bestFeature;

# Function to get the majority vote at a single location
def majorityCnt(classList):
    classCount={};
    for vote in classList:
        if vote not in classCount.keys():
            classCount = 0;
        classCount[vote] += 1;

    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=true);
    return sortedClassCount[0][0];

# Tree building code
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet];
    if classList.count(classList[0]) == len(classList):
        return classList[0];
    if len(dataSet[0]) == 1:
        return majorityCnt(classList);
    bestFeat = chooseBestFeatureToSplit(dataSet);
    bestFeatLabel = labels[bestFeat];
    myTree = {bestFeatLabel:};
    del(labels[bestFeat]);
    featValues = [example[bestFeat] for example in dataSet];
    uniqueVals = set(featValues);
    for value in uniqueVals:
        subLabels = labels[:];
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels);
    return myTree;
