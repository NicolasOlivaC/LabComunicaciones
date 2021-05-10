from prettytable import PrettyTable
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


def rle_encode(data):
    encoding = ''
    prev_char = ''
    count = 1
    if not data:
        return ''
    for char in data:
        # If the prev and current characters
        # don't match...
        if char != prev_char:
            # ...then add the count and character
            # to our encoding
            if prev_char:
                encoding += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            # Or increment our counter
            # if the characters do match
            count += 1
    else:
        # Finish off the encoding
        encoding += str(count) + prev_char
        return encoding


def rle_decode(data):
    decode = ''
    count = ''
    for char in data:
        # If the character is numerical...
        if char.isdigit():
            # ...append it to our count
            count += char
        else:
            # Otherwise we've seen a non-numerical
            # character and need to expand it for
            # the decoding
            decode += char * int(count)
            count = ''
    return decode


def startCompress(path, pathCompressed):
    timeCompress = []
    totalCompress = 0.0
    t = PrettyTable(['Archivo', 'Tiempo Compresion (Seg)'])
    for i in range(1, 31):
        entrada = open(path + str(i)+".txt", 'r').read()
        inicio = timeit.default_timer()
        encoding = rle_encode(entrada)
        final = timeit.default_timer()
        timeCompress.append(final-inicio)
        t.add_row([i, final-inicio])
        salida1 = open(pathCompressed+str(i)+"_compress"  + ".txt", 'w')
        salida1.write(encoding)
        salida1.close()
    print(t)


    for i in range(0,29):
        totalCompress += timeCompress[i]

    print("tiempo total de compresion: " + str(totalCompress) + " Seg")
    print("tiempo medio compresion: " + str(totalCompress/30)+" Seg ")


def startDecompress(pathMuestraDescomprimida):
    timeDecompress = []
    totalDecompress = 0.0
    t = PrettyTable(['Archivo', 'Tiempo Descompresion (Seg)'])
    for i in range(1, 31):

        entrada = open(pathMuestraDescomprimida + str(i)+ "_compress" + ".txt", 'r').read()

        inicio = timeit.default_timer()
        decoding=rle_decode(entrada)

        final = timeit.default_timer()
        timeDecompress.append(final-inicio)
        t.add_row([i, final-inicio])
        salida1 = open(pathMuestraDescomprimida+str(i)  +"_decompress" + ".txt", 'w')
        salida1.write(decoding)
        salida1.close()
    print(t)
    for i in range(0,1):
        totalDecompress += timeDecompress[i]

    print("tiempo total de Descompresion: " + str(totalDecompress) + " Seg")
    print("tiempo medio de Descompresion: " + str(totalDecompress/30)+" Seg ")

def startEntropy(pathMuestra, pathMuestraComprimida):
    entradaEntro = []
    salidaEntro = []
    entroEntradaProm = 0.0
    entroSalidaProm = 0.0
    compresionProm = []
    rel = 0.0
    t = PrettyTable(['Archivo', 'Original (Bytes)', 'Comprimido (Bytes)', "Diferencia (Bytes)", "Entro Original (bits)", "Entro Comprido (bits)"])
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


# configuracion inicial
pathMuestraAleatoria = "../muestrasAleatorias/"
pathMuestraRepetitiva = "../muestrasRepetitivas/"      #ruta donde obtendremos las muestras
pathCompresionRepetitiva = "./compresionRepetitiva/"   #ruta donde se guardaran las muestras comprimidas
pathCompresionAleatoria = "./compresionAleatoria/"



#Compresion Repetitiva
# startCompress(pathMuestraRepetitiva, pathCompresionRepetitiva)
# startDecompress(pathCompresionRepetitiva)
startEntropy(pathMuestraRepetitiva, pathCompresionRepetitiva)

#Compresion Aleatoria
# startCompress(pathMuestraAleatoria, pathCompresionAleatoria)
# startDecompress(pathCompresionAleatoria)
startEntropy(pathMuestraAleatoria, pathCompresionAleatoria)
