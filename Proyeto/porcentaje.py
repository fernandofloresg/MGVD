import re
import math
import os
import json
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
    #l = minusculas(l)
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




    # dicc_tf_idf = contruirifidf(dicc_tf,dicc_idf)

    sensac = open("Sensacionalista.txt")
    dicc_sensacionalista = json.loads(sensac.read())
    sensac.close()
    print(dicc_sensacionalista)
    sensac = open("NoSensacionalistas.txt")
    dicc_noSensacionalista = json.loads(sensac.read())
    sensac.close()
    print(dicc_noSensacionalista)
    aux = 20 #numero total de documentos


    while (True):
        consulta = str(input("Escribe tu consulta: "))
        consulta = procesar(consulta)
        size = len(consulta)
        dicc_cons_tf = {}
        dicc_cons_idf = {}


        for i in consulta:
            dicc_cons_tf[i]=float(consulta.count(i)) / float(size)
            #print(i , dicc_cons_tf[i])
            #print(dicc_sensacionalista)
            dicc_cons_idf[i] = 0
            consulta_counter = 0
            for j in range(25):
                new_i = i + " " + str(j)
                print(new_i)

                if new_i in dicc_sensacionalista:
                    if dicc_sensacionalista[new_i] > 0 :
                        consulta_counter += 1
                else: 
                    len_noSensacionalista = 0
                if new_i in dicc_noSensacionalista:
                    if dicc_noSensacionalista[new_i] > 0 :
                        consulta_counter += 1
                else: 
                    len_noSensacionalista = 0
                print(consulta_counter)
            if i in  dicc_cons_idf:
                dicc_cons_idf[i] = math.log10(float(aux)/float(consulta_counter))
            else : 
                dicc_cons_idf[i] = 0
        print(dicc_cons_tf,dicc_cons_idf)
        dicc_constfidf= contruirifidf(dicc_cons_tf,dicc_cons_idf)
        print(dicc_constfidf)


        q = dicc_constfidf.keys()
        r = dicc_sensacionalista.keys()
        eux = 0
        mejor = 0
        resultados = []
        for i in range(25):
            for j in q:
                myll=j+" "+str(i)
                try :
                    eux += dicc_constfidf[j] * dicc_tf_idf[myll]
                except:
                    eux = eux
            if eux > 0 :#and eux>mejor:
                print(eux)
                # l = [eux, documentosOriginales[i],i]
                # if resultados != []:
                #     if resultados[0][0]<l[0]:
                #         resultados.insert(0,l)
                #     elif resultados[-1][0]>l[0]:
                #             resultados.append(l)
                #     else:
                #         a = 0
                #         for i in resultados:
                #             if i[0]<l[0]:
                #                 resultados.insert(a,l)
                #                 break
                #             a += 1
                # else:
                #     resultados.append(l)
##                mejor = eux
##                print(eux)
##                print(documentos[i])
##                try :
##                    print(documentosOriginales[i])
##                except:
##                    print ("error al escribir el documento")
            eux = 0
        #
        # for i in resultados:
        #     print(i)
        #     print(resultados.index(i))





main()
