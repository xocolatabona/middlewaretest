from math import ceil, floor

def mergeSort(arreglo):
    if len(arreglo) > 1:
        # dividir arreglo en 2
        q = ceil(len(arreglo)/2)
        # Primera mitad
        lh = mergeSort(arreglo[:q])
        # Segunda mitad
        hh = mergeSort(arreglo[q:])
        return mezclar(lh, hh)
    else:
        return arreglo 

def mezclar(lowHalf, highHalf):
    arreglo_ordenado = []
    pointerLow = 0
    pointerHigh = 0
    while pointerLow < len(lowHalf) and pointerHigh < len(highHalf):
        if lowHalf[pointerLow] < highHalf[pointerHigh]:
            arreglo_ordenado.append(lowHalf[pointerLow])
            pointerLow += 1
        else:
            arreglo_ordenado.append(highHalf[pointerHigh])
            pointerHigh += 1
    
    if pointerLow < len(lowHalf):
        arreglo_ordenado += lowHalf[pointerLow:]
    if pointerHigh < len(highHalf):
        arreglo_ordenado += highHalf[pointerHigh:]
        
    return arreglo_ordenado

def busquedaBinaria(arreglo, elemento):
    low = 0
    high = len(arreglo) - 1
    guess = floor((high + low) / 2)
    
    if arreglo[guess] == elemento:
        return "Encontrado en la posición: " + guess
    
    while arreglo[guess] != elemento and low != high:
        if elemento < arreglo[guess]:
            #tomar la mitad de abajo
            high = guess -1
            guess = floor((high + low) / 2)
        else:
            #tomar la mitad de arriba
            low = guess + 1
            guess = floor((high + low) / 2)

        if arreglo[guess] == elemento:
            return "Encontrado en: " + str(guess)

    return "No encontrado"