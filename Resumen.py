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

    archi = open("test.txt",encoding='utf8')
    
    while (True):
        consulta = archi.read()
        #nltk.download('punkt')
        sentences = nltk.tokenize.sent_tokenize(consulta)
        consulta = procesar(consulta)
        #print(sentences)
        tokens = [nltk.tokenize.word_tokenize(s) for s in sentences]
        #print(tokens)
        print()
        #nltk.download('averaged_perceptron_tagger')
        pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]
        scores={"NN":5, "NNP":10}
        s = scores.keys()
        score = []

        #Para pasar los scores y sumar los obtenidos
        print(pos_tagged_tokens)
        for i in pos_tagged_tokens:
        	score.append([0])
        	for j in i:
        		if j[1] in s:
        			score[-1][0]+=scores[j[1]]
        print(score)


        

        #print(pos_tagged_tokens)
        size = len(consulta)
        dicc_cons_tf = {}
        dicc_cons_idf = {}

        

        for i in consulta:
            dicc_cons_tf[i]=float(consulta.count(i)) / float(size)
##            try :
##                dicc_cons_idf[i] = math.log10(float(aux)/float(len(dicc[i])))
##            except :
##                dicc_cons_idf[i]= 0

        #dicc_constfidf= contruirifidf(dicc_cons_tf,dicc_cons_idf)
        #print(dicc_cons_tf)
        print("=================================================")
        #print(consulta)
        continuar = input("Continuar")
        
main()
        
