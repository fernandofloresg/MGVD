import re
import math
import os
import json
import nltk
import numpy
from pprint import pprint  # For proper print of sequences.
import treetaggerwrapper
global stopWl
global entities

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
    lista = l.split()
    aux = []
    for i in lista:
        if len(i) > 2 and i not in stopWl:
            if i[-1]=="s":
                i =plurarASingular(i)
            aux.append(i)
    return aux

def listaToString(lista):
    texto = ""
    for elemento in lista:
        texto += " " + elemento
    return texto

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

def getEntities(txt):
    sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
    #normalized_sentences = [s.lower() for s in sentences]
    
    previous_pos = None
    current_entity_chunk = []
    all_entity_chunks = []
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='es',TAGDIR='C:/Taggers/tree-tagger-windows-3.2/TreeTagger')
    
    for s in sentences:
        tags = [treetaggerwrapper.make_tags(tagger.tag_text(s))]
        for tag in tags:
            for t in tag:
                token = t[0]
                pos   = t[1]
                if pos == previous_pos and pos.startswith('N'):
                    
                    current_entity_chunk.append(token)
                elif pos.startswith('N'):
                    if current_entity_chunk != []:
                        word = ' '.join(current_entity_chunk)
                        if(word[0].isupper()):
                            all_entity_chunks.append((' '.join(current_entity_chunk), pos))
                    current_entity_chunk = [token]
                previous_pos = pos
        
    return all_entity_chunks

def transformDictoList(dict):
    dictlist = []
    for key, value in dict.items():
        for i in range(value):
            dictlist.append(key)
    return dictlist
    
def main():
    global stopWl, dicc,entities
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

    #archi = open("test.txt",encoding='utf8')
    path = "C:\\MGVD\\TEST\\"
    files = os.listdir(path)
    aux =0
        #1) build a TreeTagger wrapper:
    

    for i in files:
        file = open(path + i,encoding="utf8")
        h = file.read()
        documentosOriginales.append(h)
        l = procesar(h) #LIMPIEZA DE LOS DATOS
        l = listaToString(l)
        print("procesando archivo: " ,aux)
        entities = getEntities(l)
        # Store the tokens as an index for the document and account for frequency.
        frec = dict()
        for c in entities:
            if c[0] in frec:
                frec[c[0]] += 1
            else:
                frec[c[0]] = 1
        l=transformDictoList(frec)
        documentos.append(l)
        diccionario(l,aux)
        # contar el tf
        size = len(l)
        for j in l:
            eux = l.count(j)
            dicc_tf[j+" "+str(aux)] = float(eux) / float(size)
        aux += 1
        
    aux +=1
    iux = 0
    print(dicc)
    for j in documentos:
        for i in j:
            dicc_idf[i+" "+str(iux)] = math.log10(float(aux)/float(len(dicc[i])))
        iux+=1

    dicc_tf_idf = contruirifidf(dicc_tf,dicc_idf)
    print("tf-ifd ----------->", dicc_tf_idf)

    
    while (True):
        consulta = str(input("Escribe tu consulta: "))
        consulta = procesar(consulta)
        size = len(consulta)
        dicc_cons_tf = {}
        dicc_cons_idf = {}
        

        for i in consulta:
            dicc_cons_tf[i]=float(consulta.count(i)) / float(size)
            try :
                dicc_cons_idf[i] = math.log10(float(aux)/float(len(dicc[i])))
            except :
                dicc_cons_idf[i]= 0

        dicc_constfidf= contruirifidf(dicc_cons_tf,dicc_cons_idf)
        
        q = dicc_constfidf.keys()
        eux = 0
        mejor = 0
        resultados = []
        for i in range(aux):
            for j in q:
                myll=j+" "+str(i)
                try :
                    eux += dicc_constfidf[j] * dicc_tf_idf[myll]
                except:
                    eux = eux
            print("puntaje: ", eux)
            if eux > 0 :#and eux>mejor:
                l = [eux, documentosOriginales[i],i]
                if resultados != []:
                    if resultados[0][0]<l[0]:
                        resultados.insert(0,l)
                    elif resultados[-1][0]>l[0]:
                            resultados.append(l)
                    else:
                        a = 0
                        for i in resultados:
                            if i[0]<l[0]:
                                resultados.insert(a,l)
                                break
                            a += 1
                else:
                    resultados.append(l)
##                mejor = eux
##                print(eux)
##                print(documentos[i])
##                try : 
##                    print(documentosOriginales[i])
##                except:
##                    print ("error al escribir el documento")
            eux = 0
        for i in resultados:
            print("El mejor resultado fue el documento con el indice",
                documentosOriginales.index(i[1]))
        
main()
        