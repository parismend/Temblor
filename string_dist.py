import re
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


def distancia_string(lista):
    arreglo = np.zeros([len(lista), len(lista)])
    for i in range(0, len(lista)):
        for j in range(i + 1, len(lista)):
            arreglo[i, j] = fuzz.token_set_ratio(
                lista[i], lista[j]
            )
    return arreglo


def indices_repetidos(lista, corte):
    arreglo = distancia_string(lista)
    return np.where(arreglo >= corte), arreglo


def checa_distancias():
    calles1 = []
    calles2 = []
    distancia = []
    for i in range(distancia_calles[0].shape[0] - 1):
        for j in range(distancia_calles[0].shape[0] - 1):
            calles1.append(distancia_calles[0][i])
            calles2.append(distancia_calles[1][j])
            distancia.append(dist[distancia_calles[0][i],
                                  distancia_calles[1][j]])

    pd.DataFrame({
        'calle1': [lista_calles[x] for x in calles1],
        'calle2': [lista_calles[x] for x in calles2],
        'distancia': distancia
    }).to_csv('datos/distancias.csv')



if __name__ == "__main__":
    df = pd.DataFrame.from_csv('datos/necesidades.csv')
    distancia_calle = indices_repetidos(df.calle.tolist(), 90)
    lista_calles = [str(df.calle.tolist()[i]) + ' ' +
                    str(df.entrecalles.tolist()[i])
                    for i in range(df.shape[0])]
    distancia_calles, dist = indices_repetidos(lista_calles, 90)
    repetidos = np.unique(distancia_calles[1])
    print(len(repetidos) / len(lista_calles))

    checa_distancias()
