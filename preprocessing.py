from nltk.stem import WordNetLemmatizer
import os
import re
import math 

# The below function is to convert any given list into vector representation list
def vectorGenerator(distinct_terms, lst):
    vector = []
    for i in range(len(distinct_terms)):
        if (distinct_terms[i] in lst):
            vector.append(lst.count(distinct_terms[i]))
        else:
            vector.append(0)
    return vector

# Calculating the amount(number of documents) for the given corpus
lst = os.listdir("Abstracts")
number_files = len(lst)
print(number_files)


terms = [] # -> saving terms for each document
distinct_terms = [] # -> saving all distinct terms from the corpus
finl_list = [] # -> This list consist of All terms lists for all documents
stop_words = [] # -> This list has all stopwords which present in Stopword-List.txt


# Getting all the stopwords from "Stopword-List.txt" and storing them in a list
sw = open("Stopword-List.txt", "r")
line = sw.read()
stop_words = line.split()
print(stop_words)


# Tokenization Process for all the documents in the corpus
i = 1
while i <= number_files:
    if i == 0: continue
    with open("Abstracts/" + str(i) + ".txt") as f:
        for line in f:
            temp = line.split()
            neww = []
            k = 0
            while (k < len(temp)):
                if temp[k].find(",") != -1:
                    splt = temp[k].split(',')
                    for j in range(len(splt)):
                        neww.append(splt[j])
                else:
                    neww.append(temp[k])
                k += 1
            temp = neww

            for words in range(len(temp)):
                remove_specialChr = "".join(re.split("[^a-zA-Z]*", temp[words]))
                remove_specialChr = remove_specialChr.lower()

                if remove_specialChr in stop_words: continue

                # Lemmatization process done here
                lemmatizer = WordNetLemmatizer()
                remove_specialChr= lemmatizer.lemmatize(remove_specialChr)

                terms.append(remove_specialChr)
                if remove_specialChr not in distinct_terms:
                    distinct_terms.append(remove_specialChr)

        terms.sort()
        while len(terms[0]) == 0: # -> if there is any empty term exist so remove that
            terms.pop(0)

        finl_list.append(terms) # -> Generating a final list containg all terms for all Documents
        terms = []

    i += 1
# while loop ends here


# checking all the document-terms list for all document (by simply printing them)
for i in range(len(finl_list)):
    print(i + 1, finl_list[i])



distinct_terms.sort()
while len(distinct_terms[0]) == 0: # -> if any empty term exist remove it..
    distinct_terms.pop(0)

print(distinct_terms)

# Saving all the distinct terms of Corpus into a text file. 
f = open("savedterms.txt", "w+")
for i in range(len(distinct_terms)):
    f.write(distinct_terms[i])
    f.write('\n')
f.close()



# Calculating Term Frequency Vectors (TF) for all Documents.
doc_vector = [] 
for i in range(len(finl_list)):
    doc_vector.append(vectorGenerator(distinct_terms, finl_list[i]))
print(doc_vector)

# calculating Inverse Document Frequency (IDF)
N= len(doc_vector)
idf = [0]*len(doc_vector[0])
for i in range (len(doc_vector)):
    for j in range (len(doc_vector[i])):
        if doc_vector[i][j] != 0:
            idf[j] += 1

for i in range (len(idf)):
    idf[i]=math.log(N/idf[i])

# multiplying TF with IDF and generating TF-IDF scores for each term in documents.
for i in range (len(doc_vector)):
    for j in range (len(doc_vector[i])):
        doc_vector[i][j] *= idf[j]
print (doc_vector)


# All Preprocessing for making TF-IDF weights Are Stored in a text file here. (So we donot Calculate that again n again).
f= open("documentVectors.txt","w")
for i in range (len(doc_vector)):
    j=0
    while (j<len(doc_vector[i])):
        f.write(str(doc_vector[i][j])+' ')
        j+=1
    f.write('\n')
f.close()

f= open("idf.txt","w")
for i in range (len(idf)):
    f.write(str(idf[i])+' ')
    j+=1
f.close()

# ------------------------Preprocessing Done here-------------------------- #