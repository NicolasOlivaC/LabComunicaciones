from prettytable import PrettyTable
from huffman import HuffmanCoding
import timeit
import os
import collections
import math
import sys



def entropy(text):
    m = len(text)
    bases = collections.Counter([tmp_base for tmp_base in text])
    entropy_value = 0
    for base in bases:
        n_i = bases[base]
        p_i = n_i / float(m)
        entropy_i = p_i * (math.log(p_i, 2))
        entropy_value += entropy_i
    return entropy_value * -1

def initCompression(path):
    timeCompress = []
    timeDecompress = []
    totalCompress = 0.0
    totalDecompress = 0.0
    t = PrettyTable(['Archivo', 'Tiempo Compresion (Seg)', 'Tiempo Descompresion (Seg)'])
    for i in range(1,31):
        #primeros parametros
        h = HuffmanCoding(path+str(i)+'.txt')
        #inicio tiempo compresion
        first=timeit.default_timer()
        output = h.compress()
        second=timeit.default_timer()
        #fin tiempo compresion
        #inicio tiempo descompresion
        first2=timeit.default_timer()
        h.decompress(output)
        second2=timeit.default_timer()
        #fin tiempo compresion

        timeCompress.append(second-first)
        timeDecompress.append(second2-first2)
        t.add_row([i, second-first, second2-first2])

        # print(str(i+1)+".- compresion: "+ str(second-first)+" Seg -- descompresion: "+str(second2-first2)+" Seg")
    print(t)

    for i in range(0,30):
        totalCompress += timeCompress[i]
        totalDecompress += timeDecompress[i]
    print("tiempo total de compresion: " + str(totalCompress)+" Seg ", " -- tiempo total descompresion: " +str(totalDecompress)+" Seg")
    print("tiempo medio compresion: " + str(totalCompress/30)+" Seg ", " -- tiempo medio descompresion: " +str(totalDecompress/30)+" Seg")

def startEntropy(path):
    entradaEntro = []
    salidaEntro = []
    entroEntradaProm = 0.0
    entroSalidaProm = 0.0
    compresionProm = []
    rel = 0.0
    t = PrettyTable(['Archivo', 'Orig (Bytes)', 'Compri (Bytes)', "Difer (Bytes)", "Entro Orig (bits)", "Entro Compri (bits)"])
    for i in range(1, 31):
        # print(i)
        tamanoOriginal = os.path.getsize(path+str(i)+".txt")
        tamanoComprimido = os.path.getsize(path+str(i)+".bin")
        compresionProm.append(tamanoComprimido)
        entrada = open(path+ str(i)+".txt", 'r').read()
        # salida = open('./muestrasRepetitivas/'+ str(i)+".bin", 'r',encoding="iso8859_2").read()
        h = HuffmanCoding(path+ str(i)+".bin")
        text = h.entropy(path+ str(i)+".bin")
        EE = entropy(entrada)
        ES = entropy(text)
        entradaEntro.append(EE) 
        salidaEntro.append(ES)
        t.add_row([i, tamanoOriginal, tamanoComprimido, tamanoOriginal-tamanoComprimido, EE, ES ])
    print(t)
    for i in range(0, 30):
        entroEntradaProm += entradaEntro[i]
        entroSalidaProm += salidaEntro[i]
        rel += compresionProm[i]
    print("Entropia promedio antes de comprimir: " + str(entroEntradaProm/30) + "bits")
    print("Entropia promedio despues de comprimir: " + str(entroSalidaProm/30) + "bits")
    print("Relacion compresion promedio " + str(((rel/30)/60000)*100))
    

pathMuestraAleatoria = "./muestrasAleatorias/"
pathMuestraRepetitiva = "./muestrasRepetitivas/"      #ruta donde obtendremos las muestras


#Compresion Repetitiva
# initCompression(pathMuestraRepetitiva)
startEntropy(pathMuestraRepetitiva)

#Compresion Aleatoria
# initCompression(pathMuestraAleatoria)
startEntropy(pathMuestraAleatoria)