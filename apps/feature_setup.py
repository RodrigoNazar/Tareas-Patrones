
import cv2
from matplotlib import pyplot as plt
from matplotlib.image import imsave
import numpy as np
import argparse
import json
import os

from utils.utils import (getThresholdImgs, printImg, isInside, segmentate,
                         extractSubmatrix)
import utils.huMoments as hu


def saveIndividualLetter(img_path):
    print('\nObteniendo las imágenes de cada letra de', img_path, '...')

    img =  cv2.imread(img_path)

    dir = 'training' if 'Training' in img_path else 'testing'

    # Obtenemos los umbrales de cada canal
    th_R, th_G, th_B = getThresholdImgs(img)

    # img = 255*((th_R > 127) | (th_G > 127) | (th_B > 127))

    # Segmentamos cada letra de la imagen
    rects = segmentate(th_R)

    options = ['A', 'S', 'D', 'F', 'G', 'X']

    # Comenzamos a clasificar cada letra
    for (x, y, w, h) in rects:

        delta = 10

        # Se despliega la letra
        current_img = extractSubmatrix(th_R, (x-delta, y-delta),
                                             (x+w+delta, y+h+delta))
        printImg(current_img, 1, 200)

        # El usuario indica que letra es
        letter = input('\n¿Que letra era esa? (Si no la viste apreta ENTER)\n\t> ')

        while letter not in options:
            print('La letra ingresada no está en las opciones (A, S, D, F, G)')
            print('Te muestro de nuevo la imagen')

            printImg(current_img, 1, 200)

            letter = input('\n¿Que letra era esa?\n\t> ')

        num = [int(pic[2:-4]) for pic in os.listdir(f'img/{dir}/{letter}')]
        num = max(num) + 1 if num else 0

        imsave(f'img/{dir}/{letter}/{letter}_{num}.png',
                cv2.merge([current_img, current_img, current_img]))


def obtainFeatures(img_path):

    print('\nObteniendo características del archivo', img_path, '...')

    img =  cv2.imread(img_path)

    # Obtenemos los umbrales de cada canal
    th_R, th_G, th_B = getThresholdImgs(img)

    # img = 255*((th_R > 127) | (th_G > 127) | (th_B > 127))

    # Segmentamos cada letra de la imagen
    rects = segmentate(th_R)

    data = {
        'img': img_path,
        'objects': []
    }

    options = ['A', 'S', 'D', 'F', 'G', 'X']

    # Comenzamos a clasificar cada letra
    for (x, y, w, h) in rects:

        delta = 22

        # Se despliega la letra
        current_img = extractSubmatrix(th_R, (x-delta, y-delta),
                                             (x+w+delta, y+h+delta))
        printImg(current_img, 1, 200)

        # El usuario indica que letra es
        letter = input('\n¿Que letra era esa? (Si no la viste apreta ENTER)\n\t> ')

        while letter not in options:
            print('La letra ingresada no está en las opciones (A, S, D, F, G)')
            print('Te muestro de nuevo la imagen')

            printImg(current_img, 1, 200)

            letter = input('\n¿Que letra era esa?\n\t> ')

        num = [int(pic[2:-4]) for pic in os.listdir('img/' + letter + '/')]
        num = max(num) + 1 if num else 0

        imsave(f'img/{letter}/{letter}_{num}.png',
                cv2.merge([current_img, current_img, current_img]))

        # Se calculan los momentos de Hu y se agrega a los datos
        # phi1, phi2, phi3, phi4, phi5, phi6, phi7 = hu.huMoments(current_img)
        # data['objects'].append(
        #     {
        #         'coord': [x, y, x+w, y+h],
        #         'letter': letter,
        #         'hu-moments': {
        #             'phi1': phi1,
        #             'phi2': phi2,
        #             'phi3': phi3,
        #             'phi4': phi4,
        #             'phi5': phi5,
        #             'phi6': phi6,
        #             'phi7': phi7
        #         }
        #      }
        # )

    # Finalmente se guarda la información de las letras
    # data_path = 'data/' + img_path[4:-4] + '_data.json'
    # print('\nGuardando los datos en: ', data_path)
    # with open(data_path, 'a') as json_file:
    #     json.dump(data, json_file, indent=2)


def setupImgsFeatures(*pics):

    print('\n1) Revisando que estén todas las imágenes segmentadas...')
    options = ['A', 'S', 'D', 'F', 'G']
    segmentadas = True

    for pic in pics:
        dir = 'training' if 'Training' in pic else 'testing'
        pic_number = 18*2*2 if dir == 'training' else 18*2
        for option in options:
            if len(os.listdir('img/' + dir + '/' + option + '/')) != pic_number:
                segmentadas = False

    if not segmentadas:
        print('\tNo están todas las imágenes pertenecientes a la prueba',end='')
        print(', es necesario segmentar...')
        for pic in pics:
            dir = 'training' if 'Training' in pic else 'testing'
            for option in options:
                for img in os.listdir('img/' + dir + '/' + option + '/'):
                    os.remove('img/' + dir + '/' + option + '/' + img)

        for pic in pics:
            saveIndividualLetter(pic)


    print('\n2) Revisando las características de cada imagen...')
    data_files = os.listdir('data/')

    # Se obtienen las características de las imágenes
    for pic in pics:
        data_path = pic[4:-4] + '_data.json'
        # Revisamos la información que ya está
        if data_path not in data_files:
            obtainFeatures(pic)
        else:
            print(f'\tLa imagen {pic} ya tiene sus características!')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tr1_path', type=str, default='img/Training_01.png',
                        help="Dirección de la imagen a procesar")
    parser.add_argument('--tr2_path', type=str, default='img/Training_02.png',
                        help="Dirección de la imagen a procesar")
    parser.add_argument('--test1_path', type=str, default='img/Testing.png',
                        help="Dirección de la imagen a procesar")
    cmd_args = parser.parse_args()
    train_setup(cmd_args.t01_path, cmd_args.t02_path, cmd_args.test1_path)
