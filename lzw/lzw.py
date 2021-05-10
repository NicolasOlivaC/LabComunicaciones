from prettytable import PrettyTable
import os
import timeit
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


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    #dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    dictionary = {chr(i): chr(i) for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dict_size = 256
    #dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    dictionary = {chr(i): chr(i) for i in range(dict_size)}
    # print(dictionary)

    w = result = compressed.pop(0)
   
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result += entry

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result

def startCompress(path, pathCompressed):
    timeCompress = []
    timeDecompress = []
    totalDecompress = 0.0
    totalCompress = 0.0
    t = PrettyTable(['Archivo', 'Tiempo compresion (Seg)', 'Tiempo descompresion (Seg)'])
    for i in range(1,31):
        entrada= open(path + str(i)+".txt",'r').read()
        inicio = timeit.default_timer()
        encoding=compress(entrada)
        fin = timeit.default_timer()
        output=open(pathCompressed + str(i)+"_compress.txt",'w')
        output.write(str(encoding).replace('[','').replace(']','').replace(' ',''))
        output.close()
        inicio2 = timeit.default_timer()
        decoding=decompress(encoding)
        fin2 = timeit.default_timer()
        timeDecompress.append(fin-inicio)
        timeCompress.append(fin2-inicio2)
        output2=open(pathCompressed + str(i)+"_decompress.txt",'w')
        output2.write(str(decoding))
        output2.close()
        t.add_row([i, fin-inicio, fin2-inicio2 ])
    
    for i in range(0,30):
        totalDecompress += timeDecompress[i]
        totalCompress += timeCompress[i]
    print(t)
    print("tiempo total de Compresion: " + str(totalCompress) + " Seg")
    print("tiempo medio de Compresion: " + str(totalCompress/30)+" Seg ")
    print("tiempo total de Descompresion: " + str(totalDecompress) + " Seg")
    print("tiempo medio de Descompresion: " + str(totalDecompress/30)+" Seg ")

def startEntropy(pathMuestra, pathMuestraComprimida):
    entradaEntro = []
    salidaEntro = []
    entroEntradaProm = 0.0
    entroSalidaProm = 0.0
    compresionProm = []
    rel = 0.0
    t = PrettyTable(['Archivo', 'Original (Bytes)', 'Comprimido (Bytes)', "Diferencia (Bytes)", "Entropia Original (bits)", "Entropia Comprimido (bits)"])
    for i in range(1, 31):
        tamanoOriginal = os.path.getsize(pathMuestra+str(i)+".txt")
        tamanoComprimido = os.path.getsize(pathMuestraComprimida+str(i)+"_compress.txt")
        compresionProm.append(tamanoComprimido)
        entrada = open(pathMuestra + str(i)+".txt", 'r').read()
        salida = open(pathMuestraComprimida + str(i)+"_compress.txt", 'r').read()
        EE = entropy(entrada)
        ES = entropy(salida)
        entradaEntro.append(EE) 
        salidaEntro.append(ES)
        t.add_row([i, tamanoOriginal, tamanoComprimido, tamanoOriginal-tamanoComprimido, EE, ES])
    print(t)
    for i in range(0, 30):
        entroEntradaProm += entradaEntro[i]
        entroSalidaProm += salidaEntro[i]
        rel += compresionProm[i]
    print("Entropia promedio antes de comprimir: " + str(entroEntradaProm/30) + "bits")
    print("Entropia promedio despues de comprimir: " + str(entroSalidaProm/30) + "bits")
    print("Relacion compresion promedio " + str(((rel/30)/60000)*100))



pathMuestraAleatoria = "../muestrasAleatorias/"
pathMuestraRepetitiva = "../muestrasRepetitivas/"      #ruta donde obtendremos las muestras
pathCompresionRepetitiva = "./compresionRepetitiva/"   #ruta donde se guardaran las muestras comprimidas
pathCompresionAleatoria = "./compresionAleatoria/"



#Compresion repetitiva
# startCompress(pathMuestraRepetitiva, pathCompresionRepetitiva)
startEntropy(pathMuestraRepetitiva, pathCompresionRepetitiva)

#Compresion aleatoria
# startCompress(pathMuestraAleatoria, pathCompresionAleatoria)
startEntropy(pathMuestraAleatoria, pathCompresionAleatoria)