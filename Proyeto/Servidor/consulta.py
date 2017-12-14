#consulta 
# -*- coding: utf-8 -*-
import re
import math
import os
import operator
global stopWl
from boilerpipe.extract import Extractor
import sys

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
    # l = minusculas(l) es posible que las paabras en mayusculas nos ayuden a diferenciar
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

def getContent(url):
    extractor = Extractor(extractor='KeepEverythingExtractor', url=url)
    return extractor.getText()

def main():
    global stopWl, dicc
    dicc = {}
    dicc_tf = {}
    dicc_idf = {}
    dicc_tf_idf= {}
    stopWl=[]
    listMain = []
    listOfWords = []
    documentos = []
    documentosOriginales = []

    stopW = open("StopWords.txt", "r+")
    stopWl = leerStopW(stopW)
    stopW.close()
    
    url = str(sys.argv[1])
    if len(url) == 0:
    	url = 'http://www.elimparcial.com/EdicionEnLinea/Notas/Nogales/13122017/1287577-VIDEO-Asesinan-a-hombre-a-balazos-en-Nogales-mujer-sobrevive.html'#url dado por vista
    consulta = getContent(url) # texto de consulta obtenida de noticia
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
    print(dicc_cons_tf, dicc_cons_idf, dicc_constfidf)

main()
