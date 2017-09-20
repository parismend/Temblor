import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


def distancia_string(lista):
    arreglo = np.zeros([len(lista), len(lista)])
    for i in range(0, len(lista)):
        for j in range(i, len(lista)):
            arreglo[i, j] = fuzz.token_set_ratio(
                lista[i], lista[j]
            )
    return arreglo


def indices_repetidos(lista, corte):
    arreglo = distancia_string(lista)
    return np.where(arreglo >= corte)[1]


if __name__ == "__main__":
    df = pd.DataFrame.from_csv('necesidades.csv')
    distancia_calle = distancia_string(df.calle.tolist())
    lista_calles = [df.calle.tolist()[i] + ' ' + df.entrecalles.tolist()[i]
                    for i in range(df.shape[0])]
    distancia_calles = distancia_string(df.calle.tolist())
