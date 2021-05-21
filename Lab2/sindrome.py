import numpy as np
import itertools
import random
from matplotlib import pyplot as plt
import difflib

def corregirBits(array):
    array = np.where(array%2 == 1, 1, array)
    array = np.where(array%2 == 0, 0, array)
    return array

def matricesIniciales(n, k):
    identidad = np.identity(k-1).astype(np.int64)
    identidad2 = np.identity(k).astype(np.int64)
    p = np.array([[1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
    pt = p.transpose()
    parity = np.concatenate((p, identidad), axis=1)
    generator = np.concatenate((identidad2, pt), axis=1)
    return  parity, generator

def posiblesPalabras(k, generator):
    bits = np.array(list(itertools.product([0, 1], repeat=k)))
    palabras = corregirBits(np.matmul(bits, generator))
    return palabras

def codificar(palabra, generadora):
    resultado = corregirBits(np.matmul(palabra, generadora))
    return resultado

def codificarCadenasA4bits(dictionary):
    for i in range (1,31):
        input = open("./input/" + str(i) + ".txt", 'r').read()
        codif = open("./codif4/" + str(i) + "_codif.txt", 'w')
        for i in input:
            if(i != "\n"):
                codif.write(dictionary[i]+" ")
        codif.close()

def codificarCadenas4bitsA7bits(generator):
    append = ""
    string2 = ""
    for i in range (1,31):
        codif4 = open("./codif4/" + str(i) + "_codif.txt", 'r').read()
        codif7 = open("./codif7/" + str(i) + "_codif7bits.txt", 'w')
        for i in codif4:
            if(i !=" "):
                append = append + i 
            else:
                array = codificar(np.array(list(append)).astype(np.int64), generator)
                for i in array:
                    string2 = string2 + str(int(i))
                codif7.write(string2 + " ")
                string2 = ""
                append = ""

def generarErrores(probError):
    cantidadErrores = 0
    cantErrores = []
    # t = PrettyTable(["Archivo", "Cantidad de errores"])
    for k in range (1,31):
        codif7 = open("./codif7/" + str(k) + "_codif7bits.txt", 'r').read()
        codif7Error = open("./codif7E001/" + str(k) + "_codif7bitsError.txt", 'w')
        for i in codif7:
            if(i != " " and random.random() <= probError):
                cantidadErrores = cantidadErrores + 1
                codif7Error.write( "1" if i=="0" else "0")
            else:
                codif7Error.write(i)
        # t.add_row([k, cantidadErrores])       
        cantErrores.append(cantidadErrores)
        cantidadErrores = 0
        codif7Error.close()
    # print(t)
    return cantErrores


def obtainSyndrom(parity, n):
    patronError = np.identity(n).astype(np.int64)
    patronError = np.concatenate(( np.matrix(np.zeros(n)), patronError)).astype(np.int64)
    sindrome = np.matmul(parity, patronError.transpose()).transpose().astype(np.int64)
    return patronError, sindrome

def defineSyndrom(secuencia, paridad):
    resultado = np.matmul(paridad, secuencia.transpose())
    resultado = np.where(resultado%2 == 1, 1, resultado)
    resultado = np.where(resultado%2 == 0, 0, resultado)
    return resultado

def corregirErrores(patronError, sindrome, paridad):
    append = ""
    string2 = ""
    cantidad = 0
    arr = []
    for i in range(1,31):
        codif7Error = open("./codif7E001/" + str(i) + "_codif7bitsError.txt", 'r').read()
        codif7ErrorDecode = open("./codif7E001/" + str(i) + "_codif7bitsRepair.txt", 'w')
        for i in codif7Error:
            if(i !=" "):
                append = append + i 
            else:
                array = np.array(list(append)).astype(np.int64)
                result = defineSyndrom(array, paridad)
                if(np.sum(result) > 0):
                    cantidad += 1
                    contador = 0
                    while True:
                        if(np.ndarray.all(result == sindrome[contador])):
                            arraym = []
                            for i in range(7):
                                arraym.append(patronError[contador].item(0,i))
                            # print(arraym)
                            break
                        else:
                            contador += 1
                    corregido = corregirBits(np.add( array, arraym))
                    # corregido = np.where(corregido%2 == 1, 1, corregido)
                    # corregido = np.where(corregido%2 == 0, 0, corregido)
                    # for i in corregido:
                    #     string2 = string2 + str(i)
                    listToStr = ''.join(map(str, corregido))
                    codif7ErrorDecode.write(listToStr + " ")
                else:
                    codif7ErrorDecode.write(append + " ")
                # string2 = ""
                append = ""
        arr.append(cantidad)
        cantidad = 0
    return arr

def decodificar7bits(diccionario):
    append = ""
    for i in range(1,31):    
        corregido = open("./codif7E001/" + str(i) + "_codif7bitsRepair.txt", 'r').read()
        decodificado = open("./codif7E001/" + str(i) + "_decodificado.txt", 'w')
        for i in corregido:
            if(i != " "):
                append = append + i
            else:
                decodificado.write(diccionario[append])
                append = ""

def comparar(pathOriginal, pathDecodif):
    contador = 0
    arr = []
    for i in range(1,31):
        original = open(pathOriginal+ str(i) + ".txt", 'r').read()
        decodificado = open(pathDecodif+ str(i) + "_decodificado.txt", 'r').read()
        for i in range(50):
            if(original[i] != decodificado[i]):
                contador += 1
        arr.append(contador)
        contador = 0
    return arr

dictionary = {
    "A": "0000",
    "B": "0001",
    "C": "0010",
    "D": "0011",
    "E": "0100",
    "F": "0101",
    "G": "0110",
    "H": "0111",
    "I": "1000",
    "J": "1001",
    "K": "1010",
    "L": "1011",
    "M": "1100",
    "N": "1101",
    "O": "1110",
    "P": "1111"
}

dictionary2 = {
    "0000000": "A",
    "0001110": "B",
    "0010101": "C",
    "0011011": "D",
    "0100011": "E",
    "0101101": "F",
    "0110110": "G",
    "0111000": "H",
    "1000111": "I",
    "1001001": "J",
    "1010010": "K",
    "1011100": "L",
    "1100100": "M",
    "1101010": "N",
    "1110001": "O",
    "1111111": "P"
}


pathInput = "./input/"
pathE001 = "./codif7E001/"

parity, generator = matricesIniciales(7, 4)
palabras = posiblesPalabras(4, generator)
print(palabras)
patronError, sindrome = obtainSyndrom(parity, 7)
codificarCadenasA4bits(dictionary)
codificarCadenas4bitsA7bits(generator)
cantErrores = generarErrores(0.1) #indicar los errores solicitados: 0.1 -- 0.01 -- 0.001
cantCorregidos = corregirErrores(patronError, sindrome, parity)
decodificar7bits(dictionary2)

resultado = comparar(pathInput, pathE001)
print(cantErrores)
print(cantCorregidos)
print(resultado)

print(f'Media: {np.mean(cantCorregidos)}')
print(f'Varianza: {np.var(cantCorregidos)}')


# por si se quiere ver con las graficas de python
# x = np.arange(1,31)
# width = 0.4  # the width of the bars
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/4, cantErrores, width, label='Cantidad de bits erroneos simulados')
# rects2 = ax.bar(x + width/5, cantCorregidos, width, label='Cantidad de palabras corregidas')
# rects3 = ax.bar(x + width/1.5, resultado, width, label='Diferencia de caracteres entre original y decodificado')
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_xticks(x)
# ax.set_xticklabels(x)


# ax.legend()
# ax.bar_label(rects1, padding=1)
# ax.bar_label(rects2, padding=1)
# ax.bar_label(rects3, padding=1)
# fig.tight_layout()
# plt.title('Simulación de transmisión con probabilidad de error del 1% en cada bit')
# plt.xlabel('Archivos .txt', fontsize=12)
# plt.ylabel('Cantidad de errores', fontsize=12)
# plt.grid(color='r', linestyle='dotted', linewidth=1)
# plt.show()

