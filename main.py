import re
import eel
import math

# import these modules
from nltk.stem import WordNetLemmatizer


# This function convert Normal list to Vector Representation 
def vectorGenerator(distinct_terms, lst):
    vector = []
    for i in range(len(distinct_terms)):
        if (distinct_terms[i] in lst):
            vector.append(lst.count(distinct_terms[i]))
        else:
            vector.append(0)
    return vector

# This function is for reading the given text file and store it into a list
def getFromFile(str):
    f = open(str, "r")
    temp = f.read()
    f.close()
    temp = temp.split()
    return temp

# This function download all the Preprocessing work[document Vectors]. (which we calculated earlier)
def get_documentVectors_from_Preprocessing():
    with open("documentVectors.txt") as f:
        dv = []
        for line in f:
            # print (i+1)
            temp = line.split()
            for i in range(len(temp)):
                temp[i] = float(temp[i])
            dv.append(temp)
    return dv


@eel.expose
def start(query):
    eel.emptytextarea()
    eel.printthere("Loading . . . . ")
    stop_words = getFromFile("Stopword-List.txt")
    distinct_terms = getFromFile("savedterms.txt")
    doc_vector = get_documentVectors_from_Preprocessing()


    querylst = [] # -> for storing the query in a list 
    temp = query.split() # -> Split the query by spaces and stores in another list
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

    # Lemitization Process done here for the given query.
    for words in range(len(temp)):
        remove_specialChr = "".join(re.split("[^a-zA-Z]*", temp[words]))
        remove_specialChr = remove_specialChr.lower()

        if remove_specialChr in stop_words: continue

        lemmatizer = WordNetLemmatizer()
        remove_specialChr = lemmatizer.lemmatize(remove_specialChr)
        querylst.append(remove_specialChr)
        
    print(querylst)

    # Converting the query into a vector represented list 
    query_vector = vectorGenerator(distinct_terms, querylst)
    idf = getFromFile("idf.txt")
    print (idf)
    for i in range (len (idf)):
        idf[i]= float (idf[i])
    

    for i in range (len(query_vector)):
        query_vector[i]*= idf[i]


    # We Apply cosine function for calculating the similarity between each document vector with the query vector 
    cosine = []
    for iter in range(len(doc_vector)):
        res = 0.0
        denomi1 = 0.0
        denomi2 = 0.0
        for i in range(len(query_vector)):
            res += doc_vector[iter][i] * query_vector[i]
            denomi1 += doc_vector[iter][i] * doc_vector[iter][i]
            denomi2 += query_vector[i] * query_vector[i]
        final_denomi = pow((denomi1 * denomi2), 0.5)
        if final_denomi==0:
            res/=0.00001
        else:
            res /= final_denomi
        cosine.append(res)

    # Show the Retrived Results
    eel.emptytextarea()
    eel.printthere("Documents Retrieved for this Query (<b>"+query+"</b>) are: <br><br>")
    flag=False
    for i in range(len(cosine)):
        if cosine[i] > 0.001:
            flag=True
            print(i + 1, ":", cosine[i])
            eel.printthere(str(i+1)+".txt &nbsp;")
    if flag == False:
        eel.printthere("Nothing Retrived....")

eel.init("Front-end")
eel.start("index.html")