from PIL import Image
from prettytable import PrettyTable
from skimage.measure.entropy import shannon_entropy
import os
import timeit

os.chdir("../muestrasIMG")
path = os.getcwd()
t = PrettyTable(['Archivo', 'Tiempo compresion (Seg)'])

def comprimir():
    timeCompress = []
    totalCompress = 0.0
    for i in range (1,31):
        image = Image.open( "C:/Users/Nico/Desktop/TareaComunicacionesDigitales/muestrasIMG/" + str(i) + ".png")
        inicio = timeit.default_timer()
        image = image.convert('RGB')
        image = image.save("C:/Users/Nico/Desktop/TareaComunicacionesDigitales/WEBP/compresion/" + str(i) + '.webp', 'WEBP', quality = 10)
        final = timeit.default_timer()
        timeCompress.append(final-inicio)
        t.add_row([i, final-inicio])
    print(t)
    for i in range(0, 29):
        totalCompress += timeCompress[i]
    print("tiempo total de compresion: " + str(totalCompress) + " Seg")
    print("tiempo medio compresion: " + str(totalCompress/30)+" Seg ")

def startEntropy():
    entradaEntro = []
    salidaEntro = []
    entroEntradaProm = 0.0
    entroSalidaProm = 0.0
    tamArch = []
    compresionProm = []
    rel = 0.0
    relArch = 0.0
    t = PrettyTable(['Archivo', 'Original (Bytes)', 'Comprimido (Bytes)', "Diferencia (Bytes)", "Entropia Original (bits)", "Entropia Comprimido (bits)"])
    for i in range(1, 31):
        tamanoOriginal = os.path.getsize("C:/Users/Nico/Desktop/TareaComunicacionesDigitales/muestrasIMG/" + str(i) + ".png")
        tamanoComprimido = os.path.getsize("C:/Users/Nico/Desktop/TareaComunicacionesDigitales/WEBP/compresion/" + str(i) + '.webp')
        tamArch.append(tamanoOriginal)
        compresionProm.append(tamanoComprimido)
        imageOriginal = Image.open( "C:/Users/Nico/Desktop/TareaComunicacionesDigitales/muestrasIMG/" + str(i) + ".png")
        imageComprimida = Image.open( "C:/Users/Nico/Desktop/TareaComunicacionesDigitales/WEBP/compresion/" + str(i) + '.webp')
        EE = shannon_entropy(imageOriginal)
        ES = shannon_entropy(imageComprimida)
        entradaEntro.append(EE) 
        salidaEntro.append(ES)
        t.add_row([i, tamanoOriginal, tamanoComprimido, tamanoOriginal-tamanoComprimido, shannon_entropy(imageOriginal), shannon_entropy(imageComprimida)])
    print(t)
    for i in range(0, 30):
        entroEntradaProm += entradaEntro[i]
        entroSalidaProm += salidaEntro[i]
        rel += compresionProm[i]
        relArch += tamArch[i]
    print("Entropia promedio antes de comprimir: " + str(entroEntradaProm/30) + "bits")
    print("Entropia promedio despues de comprimir: " + str(entroSalidaProm/30) + "bits")
    print("Relacion compresion promedio " + str(((rel/30)/(relArch/30))*100))
comprimir()
startEntropy()
