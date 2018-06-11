import re
from scipy import spatial
import math

#Create array of queries from the queries file
#generated in task 2
queryTxt = open('queries.txt', 'r')
queryTxt = (queryTxt.read()).lower()
queryTxt = re.sub(' \n', '\n', queryTxt)
queries = re.findall('<title>\n(.*)', queryTxt)

#open embedding file swap out comments based on what file is being used
embeddingTxt = open('vectors_ap8889_cbow_s300_w2_neg20_hs0_sam1e-4_iter5.txt','r')
#embeddingTxt = open('vectors_ap8889_cbow_s300_w5_neg20_hs0_sam1e-4_iter5.txt','r')
#embeddingTxt = open('vectors_ap8889_cbow_s300_w7_neg20_hs0_sam1e-4_iter5.txt','r')
#embeddingTxt = open('vectors_ap8889_skipgram_s300_w2_neg20_hs0_sam1e-4_iter5.txt','r')
#embeddingTxt = open('vectors_ap8889_skipgram_s300_w5_neg20_hs0_sam1e-4_iter5.txt','r')
#embeddingTxt = open('vectors_ap8889_skipgram_s300_w7_neg20_hs0_sam1e-4_iter5.txt','r')
embeddingtTxt = embeddingTxt.read()

#get corresponding vectors for the words into new array
embeddingWords = re.findall('([a-z]+) ', embeddingtTxt)
embeddingVectors = re.findall('[a-z]+ (.*)', embeddingtTxt)

#the array with vectors will be one big string
#convert into array of string arrays
for i in range(len(embeddingVectors)):
    embeddingVectors[i] = embeddingVectors[i].split(' ')

#remove empty string at end of array grabbed due to regex's catch all statement
#convert all the strings into float values
for i in range(len(embeddingVectors)):
    embeddingVectors[i].pop()
    embeddingVectors[i] = list(map(float, embeddingVectors[i]))

#Create dictionary with the word as the key and vector array as value 
queryDict = dict(zip(embeddingWords, embeddingVectors))

##Get set of closest terms for query=================================
#Gets corresponding vector for each query word
def getQWordVectors(query):
    qWords = query.split(' ')
    vectors = []
    for word in qWords:
        vectors.append(queryDict.get(word))
    dictionary = dict(zip(qWords, vectors))
    return dictionary

#compares two vectors and returns value
def getCosineSim(qVector, embedVector):
    try:
        return (1 - spatial.distance.cosine(qVector, embedVector))
    except:
        return (-1)

#Finds the top three words in the dictionary with the best cosine similarity for the query term
def GetClosestWord(word, vector):
    closestWord = ''
    secondClosestWord = ''
    thirdClosestWord = ''
    highestScore = int()
    secondScore = int()
    thirdScore = int()
    for key in queryDict:
        if key != word:
            score = getCosineSim(vector, queryDict.get(key))
            if score > highestScore:
                                    thirdScore = secondScore
                                    secondScore = highestScore
                                    highestScore = score
                                    thirdClosestWord = secondClosestWord
                                    secondClosestWord = closestWord
                                    closestWord = key
            elif score > secondScore:
                thirdClosestWord = secondClosestWord
                secondWord = key

                thirdScore = secondScore
                secondScore = score
            elif score > thirdScore:
                thirdClosestWord = key
                thirdScore = score
    return [closestWord, secondClosestWord]

#based on the query given, get Qterm vectors, find closest words and return
#closest words as an array.
def getSetClosestWords(query):
    queryVect = getQWordVectors(query)
    closestWords = []
    for key in queryVect:
        if key in queryDict:
            closestWords.extend(GetClosestWord(key, queryVect.get(key)))
    return closestWords
##===================================================================

##Find the top 3 matching words of a full query======================
#calculates the sum of the expansion candidates cosine similarity for all Qterms
def getTotalScore(query, embedWord):
    totalScore = int()
    qWords = query.split(' ')
    for words in qWords:
        totalScore = totalScore + getCosineSim(queryDict.get(embedWord), queryDict.get(words))
    return totalScore

#finds the three words in all the expansion candidates that best match the query
def findTopMatchingWords(query, embedWords):
    topWord = ''
    secondWord = ''
    thirdWord = ''
    topScore = int()
    secondScore = int()
    thirdScore = int()
    for word in embedWords:
        score = getTotalScore(query, word)
        if score > topScore:
            #shuffle the words down the order
            thirdWord = secondWord
            secondWord = topWord
            topWord = word
            #shuffle the scores down the order
            thirdScore = secondScore
            secondScore = topScore
            topScore = score
        elif score > secondScore:
            thirdWord = secondWord
            secondWord = word

            thirdScore = secondScore
            secondScore = score
        elif score > thirdScore:
            thirdWord = word
            thirdScore = score
    newQuery = query + " " + topWord + " " + secondWord + " " + thirdWord
    return newQuery
##===================================================================

#runs the first set of functions to Create list of closest words lists for each query
#i is used to know what query is currently being worked on.
i = 51
closestWordsQuery = []
for query in queries:
    closestWordsQuery.append(getSetClosestWords(query))
    print(i)
    i = i + 1

#create dictionary with queries as the key and expansion candidates as the value
closestQueryWords = dict(zip(queries, closestWordsQuery))

#initialise variable with string of the formating for Trec file
Qformat = '<top>\n<num>{}</num><title>\n{}\n</title>\n</top>'

#run the 2nd block of functions to find closest query terms and print to shell
#results are copied to text file
i = 51
for key in closestQueryWords:
    newQuery = findTopMatchingWords(key, closestQueryWords.get(key))
    print(Qformat.format(i, newQuery))
    i = i + 1
        
        

