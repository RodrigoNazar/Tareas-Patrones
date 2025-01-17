mod = '''
1. Extracción de Características
'''

import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime

from utils.utils import getThresholdImgs, printImg
from utils.gabor import GaborFeatures
from utils.haralick import HaralickFeatures
from utils.lbp import LBPFeatures


# Rutina de creación del vector de nombres
classes = ['rayada', 'no_rayada']
feature_names = []
for channel in ('Red ', 'Green ', 'Blue '): # Para cada canal
    # LBP features
    feature_names += [channel + 'lpb' + str(i) for i in range(59)]

    # Haralick features
    for feature in ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']:
        for dir in range(8):
            feature_names.append(channel + feature + f' dir{dir}')

    # Gabor features
    gabor = [channel + 'gabor_func' + str(i) for i in range(4)]
    for feature in gabor:
        feature_names.append(feature + ' mean')
        feature_names.append(feature + ' var')
        feature_names.append(feature + ' sum')


def FeatureComputator(img):
    '''
    Calcula el vector de característica por imagen
    '''
    
    # Obtenemos los umbrales de cada canal
    img_R, img_G, img_B = cv2.split(img)


    # FEATURE EXTRACTION

    # LBP features
    #   > 59 features por canal
    lbp_R = LBPFeatures(img_R)
    lbp_G = LBPFeatures(img_G)
    lbp_B = LBPFeatures(img_B)


    # Haralick features
    #   > 48 features por canal
    haralick_R = HaralickFeatures(img_R)
    haralick_G = HaralickFeatures(img_G)
    haralick_B = HaralickFeatures(img_B)


    # Gabor features
    #   > 12 features por canal
    gabor_R = GaborFeatures(img_R)
    gabor_G = GaborFeatures(img_G)
    gabor_B = GaborFeatures(img_B)


    # Features por canal
    features_R = np.concatenate((lbp_R, haralick_R, gabor_R))
    features_G = np.concatenate((lbp_G, haralick_G, gabor_G))
    features_B = np.concatenate((lbp_B, haralick_B, gabor_B))


    # Vector final de features, de lago (59 + 48 + 12)*3 = 357
    return np.concatenate((features_R, features_G, features_B)).tolist()



def FeatureExtractor(training_path='img/training',
                     testing_path='img/testing',
                     classes=classes):
        '''
        Genera el JSON de las características de cada imagen.
        Este tiene la siguiente estructura:
        {
            'feature_names': Lista de nombres de las features,
            'feature_values_train': matriz de features de training,
            'labels_train': Vector de etiquetas de cada una de las muestras de training,
            'feature_values_test': matriz de features de testing,
            'labels_test': Vector de etiquetas de cada una de las muestras de testing,

        }
        '''

        print('\nObteniendo las características ...')

        # Si ya se calcularon las características, sólo las consultamos
        existsData = os.listdir('data/')
        if 'paredes_data.json' in existsData:
            print('Se encontraron características ya calculadas!')
            with open(os.path.join('data/', 'paredes_data.json'), 'r') as file:
                return json.loads(file.read())

        # Si no se han calculado las características, lo hacemos
        print('Calculando las características de las imágenes:\n')
        data = {
            'feature_names': feature_names,
            'feature_values_train': [],
            'labels_train': [],
            'feature_values_test': [],
            'labels_test': [],

        }

        start = datetime.now()
        i = 1
        for _class in classes:

            # Características de las imágenes de training
            dir_path = os.listdir(os.path.join(training_path, _class))
            for img in dir_path:

                img_path = os.path.join(training_path, _class, img)
                img = cv2.imread(img_path)

                print(f'Procesando {img_path}, imagen número {i}/10000')

                # Calculamos el vector de características
                features = FeatureComputator(img)
                # Etiqueta de la muestra
                label = 1 if _class == 'rayada' else 2

                data['feature_values_train'].append(features)
                data['labels_train'].append(label)
                i += 1

            # Características de las imágenes de testing
            dir_path = os.listdir(os.path.join(testing_path, _class))
            for img in dir_path:

                img_path = os.path.join(testing_path, _class, img)
                img = cv2.imread(img_path)
                print(f'Procesando {img_path}, imagen número {i}/10000')

                # Calculamos el vector de características
                features = FeatureComputator(img)
                # Etiqueta de la muestra
                label = 1 if _class == 'rayada' else 2

                data['feature_values_test'].append(features)
                data['labels_test'].append(label)

                i += 1

        # Finalmente guardamos los datos en un archivo
        with open('data/paredes_data.json', 'w') as json_file:
            json_file.write(json.dumps(data))

        # En mi máquina se demoró 38:40.71 minutos
        print('Tiempo tomado por la extracción: ', datetime.now() - start)

        return data


if __name__ == '__main__':
    print(mod)
