from numpy import *
import operator
from os import listdir

# Creates a test Dataset.
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]]);
    labels = ['A','A','B','B'];
    return group, labels;


# Classifies inX according to the given dataSet and its corresponding Labels.
# Then does a vote with the k Lowest to make a decision
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0];
    diffMat = tile(inX, (dataSetSize,1)) - dataSet;                             #------------------------------
    sqDiffMat = diffMat**2;                                                     #
    sqDistances = sqDiffMat.sum(axis=1)                                         #   Distance Calculations
    distances = sqDistances**0.5;                                               #
    sortedtDistIndicies = distances.argsort();                                  #------------------------------
    classCount={};

    for i in range(k):
        voteILabel = labels[sortedtDistIndicies[i]];                            #
        classCount[voteILabel] = classCount.get(voteILabel, 0) + 1;             #   Voting with lowest k distances
    # Sorting Dict.
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True);
    return sortedClassCount[0][0];

# Text Record to numPy parsing code.
def file2matrix(filename):
    fr = open(filename);
    numberOfLines = len(fr.readlines());
    returnMat = zeros((numberOfLines,3));
    classLabelVector = [];
    fr = open(filename);
    index = 0;
    for line in fr.readlines():
        line = line.strip();
        listFromLine = line.split('\t');
        returnMat[index,:] = listFromLine[0:3];
        classLabelVector.append(listFromLine[-1]);
        index += 1;
    return returnMat, classLabelVector;

# Data normalizing code.
def autoNorm(dataSet):
    minVals = dataSet.min(0);
    maxVals = dataSet.max(0);
    ranges = maxVals - minVals;
    normDataSet = zeros(shape(dataSet));
    m = dataSet.shape[0];
    normDataSet = dataSet - tile(minVals, (m,1));
    normDataSet = normDataSet/tile(ranges, (m,1));
    return normDataSet, ranges, minVals;

# Classifer Testing Code for dating site.
def datingClassTest():
    hoRatio = 0.10;
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt');
    normMat, ranges, minVals = autoNorm(datingDataMat);
    m = normMat.shape[0];
    numTestVecs = int(m*hoRatio);
    errorCount = 0.0;
    for i in range(numTestVecs):
        classfierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m],3);
        print("the classifier came back with: %s, the real answer is: %s" % (classfierResult, datingLabels[i]));
        if(classfierResult != datingLabels[i]) : errorCount += 1;
    print("the total error was %f" % (errorCount/float(numTestVecs)));

# Function to check if you will like a person. Based off of provided input.
def classifyPerson():
    percentTats = float(input("Percentage of time playing video games? "));
    ffmiles = float(input("Frequent filer miles earned per year? "));
    iceCream = float(input("liters of icecream consumed per year? "));
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt');
    normMat, ranges, minVals = autoNorm(datingDataMat);
    inArr = array([ffmiles, percentTats, iceCream]);
    classifierResult = classify0((inArr-minVals)/ranges, normMat, datingLabels, 3);
    print("You will probably like this person: %s" % (classifierResult));

# Converts an 32 x 32 image to a vector.
def img2vector(filename):
    returnVect = zeros((1,1024));
    fr = open(filename);
    for i in range(32):
        lineStr = fr.readline();
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j]);
    return returnVect;

# Unit test for handwriting checking.
def handwritingClassTest():
    hwLabels = [];
    trainingFileList = listdir('trainingDigits');
    m = len(trainingFileList);
    trainingMat = zeros((m, 1024));
    for i in range(m):
        fileNameStr = trainingFileList[i];
        fileStr = fileNameStr.split('.')[0];
        classNumStr = int(fileStr.split('_')[0]);
        hwLabels.append(classNumStr);
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr);
    testFileList = listdir('testDigits');
    errorCount = 0.0;
    mTest = len(testFileList);
    for i in range(mTest):
        fileNameStr = testFileList[i];
        fileStr = fileNameStr.split('.')[0];
        classNumStr = int(fileStr.split('_')[0]);
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr);
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3);
        print("The classifier came back with %d, the real answer is %d" % (classifierResult, classNumStr));
        if(classifierResult != classNumStr) : errorCount += 1;

    print("The total number of errors is: %d" % errorCount);
    print("The total error rate is: %f" % (errorCount/float(mTest)));
