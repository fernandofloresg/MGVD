# -*- coding: utf-8 -*-
import re
import math
import os
import csv, operator
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

    #archi = open("test.txt",encoding='utf8')
    path = "/home/david/Escritorio/MGVD/MGVD/testProyect/"
    files = os.listdir(path)
    aux =0

    # Recorremos todas las noticias para obtener todas
    # las palabras, lo cual sera la primera linea del
    # documento de salida
    for i in files:
        file = open(path + i, encoding = "utf-8")
        file = file.read()
        # documentosOriginales.append(h)
        file = procesar(file)
        for word in file:
            if word not in listOfWords:
            	# Cada palabra de almacena en una lista
                listOfWords.append(word)
    # La lista se palabras se almacena en una lista principal
    # Se utilizara mas adelante
    listMain.append(listOfWords)

    # Se construye el dicc de tf
    for i in files:
        file = open(path + i, encoding = "utf-8")
        h = file.read()
        documentosOriginales.append(h)
        l = procesar(h)
        documentos.append(l)
        diccionario(l,aux)
        # print(l)
        # contar el tf
        size = len(l)
        for j in l:
            eux = l.count(j)
            dicc_tf[j+" "+str(aux)] = float(eux) / float(size)
        aux += 1

    aux +=1
    iux = 0
    # Se construye el diccionario idf
    for j in documentos:
        for i in j:
            dicc_idf[i+" "+str(iux)] = math.log10(float(aux)/float(len(dicc[i])))
        iux+=1

    #Se construye el dicionario tf-idf
    dicc_tf_idf = contruirifidf(dicc_tf,dicc_idf)
    
    aux = 0
    # Nuevamente recorremos todos las noticias para obtener
    # el puntaje de su tf-idf
    for i in files:
        file = open(path + i, encoding = "utf-8")
        file = file.read()
        file = procesar(file)
        listaux = []
        size = float(len(file))
        for j in listOfWords:
            mykey = j +" "+str(aux)
            try:
                listaux.append(str(dicc_tf_idf[mykey]))
            except :
                listaux.append("0")
        # Estos puntajes se almacenan en una lista auxiliar
        # Cada una de estas representa un documeto
        listMain.append(listaux)
        aux += 1
    
    # Creamos un archivo
    # Recorremos la lista principal y cada una de sus
    # sub-listas sera un renglo en el documento
    print(listMain[0])
    with open("output.cvs","w") as out:
        for list in listMain:
            aux = ""
            for p in list:
                aux += p + ","
            aux = aux[:-1]
            aux += "\n"
            out.write(aux)

main()
