import re
import math
import os
import json
global stopWl
import sys
from boilerpipe.extract import Extractor

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

def getContent(url):
    extractor = Extractor(extractor='KeepEverythingExtractor', url=url)
    return extractor.getText()

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
    sensac = open("dicc_S.txt")
    dicc_S = json.loads(sensac.read())
    # print(dicc_sensacionalista)
    sensac.close()
    sensac = open("NoSensacionalistas.txt")
    dicc_noSensacionalista = json.loads(sensac.read())
    # print(dicc_sensacionalista)

    aux = 22
    url = str(sys.argv[1])
    if len(url) == 0:
        url = 'www.uabc.edu.mx'#url dado por vista
    consulta = getContent(url) # texto de consulta obtenida de noticia
    text_entry = 'Ford de México descartó el traslado de la producción de la nueva generación del modelo Fusion a China, es decir, el modelo 2018, pero no aclaró si a partir de 2019 este vehículo ya no se fabricará en Hermosillo. Este miércoles, la agencia Reuters dio a conocer que Ford planea consolidar la producción global del Fusion en China a partir del 2020 y de ahí exportarlos hacia Estados Unidos y Europa. "No tenemos planes de exportar la nueva generación del Fusion desde China a Norte América o Europa". "Fusion es una parte importante de nuestro portafolio de automóviles. Tendremos más información para compartir de la nueva generación del Fusion mas adelante", indicó Ford vía correo electrónico. De enero a noviembre, Ford fabricó 124 mil 612 unidades de Fusion, 52% menos que en el mismo periodo del año anterior cuando produjo 258 mil 596 unidades. Medios locales en Hermosillo reportaron hace algunas semanas que Ford planea recortar 600 puestos de trabajo en la planta por cambios en la línea de producción.'
    consulta = procesar(consulta)
    size = len(consulta)
    dicc_cons_tf = {}
    dicc_cons_idf = {}


    for i in consulta:
        dicc_cons_tf[i]=float(consulta.count(i)) / float(size)
        try :
            dicc_cons_idf[i] = math.log10(float(aux)/float(len(dicc_S[i])))
        except :
            dicc_cons_idf[i]= 0

    dicc_constfidf= contruirifidf(dicc_cons_tf,dicc_cons_idf)

        # print(dicc_cons_tf)
        # print(dicc_cons_idf)

        # print(dicc_constfidf)
    q = dicc_constfidf.keys()
    r = dicc_sensacionalista.keys()
    eux = 0
    mejor = 0
    list_score_S=[]
    list_score_NS=[]

    resultados = []
    for i in range(aux):
        for j in q:
            myll=j+" "+str(i)
            try :
                eux += dicc_constfidf[j] * dicc_sensacionalista[myll]
                    # print(eux)
            except:
                eux = eux
        if eux > 0 :#and eux>mejor:
            list_score_S.append(eux)
        list_score_S.sort()
        eux = 0
    for i in range(aux):
        for j in q:
            myll=j+" "+str(i)
            try :
                eux += dicc_constfidf[j] * dicc_noSensacionalista[myll]
                    # print(eux)
            except:
                eux = eux
        if eux > 0 :#and eux>mejor:
            list_score_NS.append(eux)
        list_score_NS.sort()
        eux = 0
    S = 0
    NS = 0
    for i in range(20):
        try:
            if list_score_S[-1] > list_score_NS[-1]:
                S += 1
                list_score_S.pop()
            else:
                NS += 1
                list_score_NS.pop()
        except :
            pass 

    porcentaje = (S * 100)/20
    print(porcentaje)
main()
