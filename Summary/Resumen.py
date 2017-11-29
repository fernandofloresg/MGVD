import re
import math
import nltk
global stopWl

def acentos(s):
    ac = ["á","é","í","ó","ú","ñ"]
    s = s.replace(ac[0],"a")
    s = s.replace(ac[1],"e")
    s = s.replace(ac[2],"i")
    s = s.replace(ac[3],"o")
    s = s.replace(ac[4],"u")
    s = s.replace(ac[5],"n")
    return s

def minusculas(s):
    return s.lower()

def diccionario(lista,num):
    global dicc
    for i in lista:
        if i in dicc:
            dicc[i].append(num)
        else:
            dicc[i] = []
            dicc[i].append(num)
            
def plurarASingular(palabra):
    if len(palabra)> 3 and palabra[-2] == 'e':
        if palabra[-3] in ['i','u','b','c','g','m','p','t']:
            palabra = palabra[0:-2]
    if palabra[-1] == 's'and palabra[-2] in ['a','e','o','u']:
            palabra = palabra[0:-1]
    return palabra

    

def procesar(i):
    global stopWl
    l = acentos(i)
    l= re.sub('\W+',' ',l)
    l = minusculas(l)
    lista = l.split()
    aux = []
    for i in lista:
        if len(i) > 2 and i not in stopWl:
            if i[-1]=="s":
                i =plurarASingular(i)
            aux.append(i)
    return aux

def contruirifidf(tf,idf):
    llaves = tf.keys()
    dicc = {}
    for i in llaves:
        dicc[i] = tf[i]*idf[i]
        #print(i," : ", dicc[i])
    return dicc
        
def leerStopW(archi):
    stopWl =[]
    for i in archi.readlines():
        i=i[0:-1]
        stopWl.append(i)
    return stopWl 

def searchmin(lista,lim):
	minimo = 0
	print(lista)
	for i in range(len(lista)):
		print(i)
		if lista[i][0]<lista[minimo][0]:
			minimo=i
	return minimo

    
    
def main():
    global stopWl, dicc
    dicc = {}
    dicc_tf = {}
    dicc_idf = {}
    dicc_tf_idf= {}
    stopWl=[]
    documentos = []
    documentosOriginales = []
    
    stopW = open("StopWords.txt", "r+")
    stopWl = leerStopW(stopW)
    stopW.close()
  
    archi = open("ensenada.txt",encoding='utf8')
    
    while (True):
        consulta = archi.read()
        #nltk.download('punkt')
        sentences = nltk.tokenize.sent_tokenize(consulta)
        consulta = procesar(consulta)
        #print(sentences)
        tokens = [nltk.tokenize.word_tokenize(s) for s in sentences]
        #print(tokens)
        print()
        # nltk.download('averaged_perceptron_tagger')
        pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
        scores={"CC":1,
        		"CD":1,
        		"DT":2,
        		"EX":2,
        		"FW":5,
        		"IN":1,
        		"JJ":3,
        		"JJR":2,
        		"JJS":2,
        		"LS":1,
        		"MD":7,
        		"NN":5,
        		"NNP":8,
        		"NNPS":7,
        		"PDT":5,
        		"PRP":6,
        		"PR$":3,
        		"RB":3,
        		"RP":1,
        		"UH":1,
        		"VB":9,
        		"VBD":8,
        		"VBG":8,
        		"VBN":7,
        		"VBP":7,
        		"VBZ":8
        		}
        s = scores.keys()
        score = []
        to=len(sentences)
        p=50
        numSentSelecc = int(p * to / 100)

        # print(pos_tagged_tokens)
        mini = 0
        sentSelecc=[]
        for i in pos_tagged_tokens:
        	score.append(0)
        	for j in i:
        		if j[1] in s:
        			score[-1]+=scores[j[1]]

        print(score)

        for i in range(numSentSelecc):
        	sentSelecc.append(score.index(max(score)))
        	score[sentSelecc[-1]]=0

        sentSelecc.sort()
        print(sentSelecc)

        #print(pos_tagged_tokens)
        size = len(consulta)
        dicc_cons_tf = {}
        dicc_cons_idf = {}

        

        for i in sentSelecc:
        	print(sentences[i])
            
        continuar = input("Continuar")
        
main()
        
