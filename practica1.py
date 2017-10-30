import re
import math
import os
global stopWl

def intersect(l1,l2):
    answer = []
    for i in l1:
        if i in l2:
            answer.append(i)
    return answer



def insertar(nodo, lista):
    for i in range(len(lista)):
       # print(i)
        if lista[i]>nodo:
            lista.insert(i,nodo)
    return(lista)
            

def union(l1,l2):
    for i in l1:
        if i not in l2:
            l2 = insertar(i,l2)
    return(l2)

def diference(l1,l2):
    answer = []
    for i in l1:
        if i not in l2 :
            answer.append(i)
    return answer

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
        
def leerStopW(archi):
    stopWl =[]
    for i in archi.readlines():
        i=i[0:-1]
        stopWl.append(i)
    return stopWl    
    
    
def main():
    global stopWl, dicc
    dicc = {}

    stopW = open("StopWords.txt", "r+")
    stopWl = leerStopW(stopW)
    stopW.close()

    files = os.listdir()
    files.remove('practica1.py')
    files.remove('StopWords.txt')
    #print(files)
    aux = 0
    for i in files:
        file = open(i)
        for j in file.readlines():
            line = procesar(j)
            diccionario(line,aux)
        aux += 1

    #print(dicc)
    
    print("intesección: 1")
    print("union:       2")
    print("diferencia:  3")
    while True:
        palabra1 = input("primera palabra: ")
        palabra2 = input("segunda palabra: ")
        opc = int(input("Cual es tu opcion: "))
        if opc == 1:
            print (intersect(dicc[palabra1],dicc[palabra2]))
        elif opc == 2:
            print (union(dicc[palabra1],dicc[palabra2]))
        elif opc ==3:
            print (diference(dicc[palabra1],dicc[palabra2]))
        else:
            break

main()
        
