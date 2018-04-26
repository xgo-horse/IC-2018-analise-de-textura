#!python3

"""
O script_preenchido.py gera a partir das imagens geradas pelo script_borders uma imagem
cujo interior é pintado de azul.

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from enum import Enum


class location(Enum):
    NORTH = 1
    SOUTH = 2
    LEFT = 3
    RIGHT = 4



# Altera a pasta de trabalho e cria uma lista com todas as imagens
os.chdir('granito/alterado/')
lista_imagens = sorted(os.listdir('.'))

# Loop de leitura de todas as imagens na pasta

for entry in lista_imagens:
    
    # print(entry)
    string = str(entry)
    if string.find("borders") >= 0:
        continue
    if string.find("preenchido") >= 0:
        continue
    # Leitura da imagem
    img = cv2.imread(entry, cv2.IMREAD_COLOR)

    # Pega o total X e Y da imagem e calcula o ponto central
    y, x, z = img.shape
    new_img = cv2.imread((str(entry)+"_borders"), cv2.IMREAD_COLOR)
    middlex = x // 2
    middley = y // 2
    current_x = middlex
    current_y = middley
    loc = location.NORTH
    front_wall = False
    left_wall = False

    while front_wall is False:
        # Bloco de verificação de borda a frente
        if loc == location.NORTH:
            pixel_b = img.item(current_y - 1, current_x, 0)
            pixel_g = img.item(current_y - 1, current_x, 1)
            pixel_r = img.item(current_y - 1, current_x, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_y += -1
                front_wall = False

        elif loc == location.RIGHT:
            pixel_b = img.item(current_y, current_x + 1, 0)
            pixel_g = img.item(current_y, current_x + 1, 1)
            pixel_r = img.item(current_y, current_x + 1, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_x += 1
                front_wall = False

        elif loc == location.SOUTH:
            pixel_b = img.item(current_y + 1, current_x, 0)
            pixel_g = img.item(current_y + 1, current_x, 1)
            pixel_r = img.item(current_y + 1, current_x, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_y += 1
                front_wall = False

        elif loc == location.LEFT:
            pixel_b = img.item(current_y, current_x - 1, 0)
            pixel_g = img.item(current_y, current_x - 1, 1)
            pixel_r = img.item(current_y, current_x - 1, 2)
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
                front_wall = True
            else:
                current_x += -1
                front_wall = False


    # Vira à direita
    i = current_x
    j = current_y
    test_pixel = new_img.item(j, i, 0)
    while test_pixel == 0:
        new_img.itemset((j, i, 0), 170)
        new_img.itemset((j, i, 1), 0)
        new_img.itemset((j, i, 2), 0)
        j += 1
        test_pixel = new_img.item(j, i, 0)
        
    init_x = current_x
    init_y = current_y
    if loc == location.LEFT:
        pass
    elif loc == location.NORTH:
        # Vira à direita
        loc = location.RIGHT
    elif loc == location.RIGHT:
        pass
    elif loc == location.SOUTH:
        pass
    
    ##############################################################################################
    # Olha o pixel a frente
    pixel_b = img.item(current_y, current_x + 1, 0)
    pixel_g = img.item(current_y, current_x + 1, 1)
    pixel_r = img.item(current_y, current_x + 1, 2)
    # Se tem uma borda
    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
        
        # Pinta o pixel à frente
        i = current_x
        j = current_y
        test_pixel = new_img.item(j, i, 0)
        while test_pixel == 0:
            new_img.itemset((j, i, 0), 170)
            new_img.itemset((j, i, 1), 0)
            new_img.itemset((j, i, 2), 0)
            j += 1
            test_pixel = new_img.item(j, i, 0)
        # Vira para o Sul
        loc = location.SOUTH

        # Olha o pixel à frente
        pixel_b = img.item(current_y + 1, current_x, 0)
        pixel_g = img.item(current_y + 1, current_x, 1)
        pixel_r = img.item(current_y + 1, current_x, 2)

        # Se tem uma borda
        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
            
            # Pinta o pixel à frente
            i = current_x
            j = current_y
            test_pixel = new_img.item(j, i, 0)
            while test_pixel == 0:
                new_img.itemset((j, i, 0), 170)
                new_img.itemset((j, i, 1), 0)
                new_img.itemset((j, i, 2), 0)
                j += 1
                test_pixel = new_img.item(j, i, 0)
                
            # Vira à esquerda
            loc = location.LEFT

            # Olha o pixel à frente
            pixel_b = img.item(current_y, current_x - 1, 0)
            pixel_g = img.item(current_y, current_x - 1, 1)
            pixel_r = img.item(current_y, current_x - 1, 2)

            # Se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
               
                # Pinta a borda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

            # Senão anda para a esquerda
            else:
                current_x += -1

        # Senao anda ao Sul
        else:

            current_y += 1

    # Senao anda à direita
    else:

        current_x += 1
    while current_x != init_x or current_y != init_y:
        if loc == location.RIGHT:

            # Olha o pixel à esquerda
            pixel_b = img.item(current_y-1, current_x, 0)
            pixel_g = img.item(current_y-1, current_x, 1)
            pixel_r = img.item(current_y-1, current_x, 2)

            # Verifica se tem uma borda

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y, current_x + 1, 0)
                pixel_g = img.item(current_y, current_x + 1, 1)
                pixel_r = img.item(current_y, current_x + 1, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para o Sul
                    loc = location.SOUTH

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y + 1, current_x, 0)
                    pixel_g = img.item(current_y + 1, current_x, 1)
                    pixel_r = img.item(current_y + 1, current_x, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)
                            
                        # Vira à esquerda
                        loc = location.LEFT

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y, current_x - 1, 0)
                        pixel_g = img.item(current_y, current_x - 1, 1)
                        pixel_r = img.item(current_y, current_x - 1, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para a esquerda
                        else:
                            current_x += -1

                    # Senao anda ao Sul
                    else:

                        current_y += 1

                # Senao anda à direita
                else:

                    current_x += 1

            #Senao anda para o norte
            else:
                loc = location.NORTH
                current_y += -1

        elif loc == location.NORTH:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y, current_x-1, 0)
            pixel_g = img.item(current_y, current_x-1, 1)
            pixel_r = img.item(current_y, current_x-1, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y-1, current_x, 0)
                pixel_g = img.item(current_y-1, current_x, 1)
                pixel_r = img.item(current_y-1, current_x, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para a direita
                    loc = location.RIGHT

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y, current_x+1, 0)
                    pixel_g = img.item(current_y, current_x+1, 1)
                    pixel_r = img.item(current_y, current_x+1, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para o sul
                        loc = location.SOUTH

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y+1, current_x, 0)
                        pixel_g = img.item(current_y+1, current_x, 1)
                        pixel_r = img.item(current_y+1, current_x, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para o sul
                        else:
                            current_y += 1

                    # Senao anda para a direita
                    else:

                        current_x += 1

                # Senao anda para o norte
                else:

                    current_y += -1

            #Senão anda para a esquerda
            else:
                loc = location.LEFT
                current_x += -1


        elif loc == location.SOUTH:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y, current_x+1, 0)
            pixel_g = img.item(current_y, current_x+1, 1)
            pixel_r = img.item(current_y, current_x+1, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 255)
                    new_img.itemset((j, i, 1), 255)
                    new_img.itemset((j, i, 2), 255)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y+1, current_x, 0)
                pixel_g = img.item(current_y+1, current_x, 1)
                pixel_r = img.item(current_y+1, current_x, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para a esquerda
                    loc = location.LEFT

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y, current_x-1, 0)
                    pixel_g = img.item(current_y, current_x-1, 1)
                    pixel_r = img.item(current_y, current_x-1, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para o norte
                        loc = location.NORTH

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y-1, current_x, 0)
                        pixel_g = img.item(current_y-1, current_x, 1)
                        pixel_r = img.item(current_y-1, current_x, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para o norte
                        else:
                            current_y += -1

                    # Senao anda para a esquerda
                    else:

                        current_x += -1

                # Senao anda para o sul
                else:

                    current_y += 1

            #Senão anda para a direita
            else:
                loc = location.RIGHT
                current_x += 1




        elif loc == location.LEFT:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y+1, current_x, 0)
            pixel_g = img.item(current_y+1, current_x, 1)
            pixel_r = img.item(current_y+1, current_x, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)
                    
                # Olha o pixel à frente
                pixel_b = img.item(current_y, current_x-1, 0)
                pixel_g = img.item(current_y, current_x-1, 1)
                pixel_r = img.item(current_y, current_x-1, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para o norte
                    loc = location.NORTH

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y-1, current_x, 0)
                    pixel_g = img.item(current_y-1, current_x, 1)
                    pixel_r = img.item(current_y-1, current_x, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para a direita
                        loc = location.RIGHT

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y, current_x+1, 0)
                        pixel_g = img.item(current_y, current_x+1, 1)
                        pixel_r = img.item(current_y, current_x+1, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)
                                
                        # Senão anda para o direita
                        else:
                            current_x += 1

                    # Senao anda para o norte
                    else:

                        current_y += -1

                # Senao anda para esquerda
                else:

                    current_x += -1

            #Senão anda para o sul
            else:
                loc = location.SOUTH
                current_y += 1
    print("Bordas de " + str(entry) + " calculadas")
    cv2.imwrite(str(entry)+"_preenchido", new_img)


# Altera a pasta de trabalho e cria uma lista com todas as imagens
os.chdir('../nao_alterado/')
lista_imagens = sorted(os.listdir('.'))

# Loop de leitura de todas as imagens na pasta

for entry in lista_imagens:
    
    # print(entry)
    string = str(entry)
    if string.find("borders") >= 0:
        continue
    if string.find("preenchido") >= 0:
        continue
    # Leitura da imagem
    img = cv2.imread(entry, cv2.IMREAD_COLOR)

    # Pega o total X e Y da imagem e calcula o ponto central
    y, x, z = img.shape
    new_img = cv2.imread((str(entry)+"_borders"), cv2.IMREAD_COLOR)
    middlex = x // 2
    middley = y // 2
    current_x = middlex
    current_y = middley
    loc = location.NORTH
    front_wall = False
    left_wall = False

    while front_wall is False:
        # Bloco de verificação de borda a frente
        if loc == location.NORTH:
            pixel_b = img.item(current_y - 1, current_x, 0)
            pixel_g = img.item(current_y - 1, current_x, 1)
            pixel_r = img.item(current_y - 1, current_x, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_y += -1
                front_wall = False

        elif loc == location.RIGHT:
            pixel_b = img.item(current_y, current_x + 1, 0)
            pixel_g = img.item(current_y, current_x + 1, 1)
            pixel_r = img.item(current_y, current_x + 1, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_x += 1
                front_wall = False

        elif loc == location.SOUTH:
            pixel_b = img.item(current_y + 1, current_x, 0)
            pixel_g = img.item(current_y + 1, current_x, 1)
            pixel_r = img.item(current_y + 1, current_x, 2)

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                front_wall = True
            else:
                current_y += 1
                front_wall = False

        elif loc == location.LEFT:
            pixel_b = img.item(current_y, current_x - 1, 0)
            pixel_g = img.item(current_y, current_x - 1, 1)
            pixel_r = img.item(current_y, current_x - 1, 2)
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
                front_wall = True
            else:
                current_x += -1
                front_wall = False


    # Vira à direita
    i = current_x
    j = current_y
    test_pixel = new_img.item(j, i, 0)
    while test_pixel == 0:
        new_img.itemset((j, i, 0), 170)
        new_img.itemset((j, i, 1), 0)
        new_img.itemset((j, i, 2), 0)
        j += 1
        test_pixel = new_img.item(j, i, 0)
        
    init_x = current_x
    init_y = current_y
    if loc == location.LEFT:
        pass
    elif loc == location.NORTH:
        # Vira à direita
        loc = location.RIGHT
    elif loc == location.RIGHT:
        pass
    elif loc == location.SOUTH:
        pass
    
    ##############################################################################################
    # Olha o pixel a frente
    pixel_b = img.item(current_y, current_x + 1, 0)
    pixel_g = img.item(current_y, current_x + 1, 1)
    pixel_r = img.item(current_y, current_x + 1, 2)
    # Se tem uma borda
    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
        
        # Pinta o pixel à frente
        i = current_x
        j = current_y
        test_pixel = new_img.item(j, i, 0)
        while test_pixel == 0:
            new_img.itemset((j, i, 0), 170)
            new_img.itemset((j, i, 1), 0)
            new_img.itemset((j, i, 2), 0)
            j += 1
            test_pixel = new_img.item(j, i, 0)
        # Vira para o Sul
        loc = location.SOUTH

        # Olha o pixel à frente
        pixel_b = img.item(current_y + 1, current_x, 0)
        pixel_g = img.item(current_y + 1, current_x, 1)
        pixel_r = img.item(current_y + 1, current_x, 2)

        # Se tem uma borda
        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
            
            # Pinta o pixel à frente
            i = current_x
            j = current_y
            test_pixel = new_img.item(j, i, 0)
            while test_pixel == 0:
                new_img.itemset((j, i, 0), 170)
                new_img.itemset((j, i, 1), 0)
                new_img.itemset((j, i, 2), 0)
                j += 1
                test_pixel = new_img.item(j, i, 0)
                
            # Vira à esquerda
            loc = location.LEFT

            # Olha o pixel à frente
            pixel_b = img.item(current_y, current_x - 1, 0)
            pixel_g = img.item(current_y, current_x - 1, 1)
            pixel_r = img.item(current_y, current_x - 1, 2)

            # Se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:
               
                # Pinta a borda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

            # Senão anda para a esquerda
            else:
                current_x += -1

        # Senao anda ao Sul
        else:

            current_y += 1

    # Senao anda à direita
    else:

        current_x += 1
    while current_x != init_x or current_y != init_y:
        if loc == location.RIGHT:

            # Olha o pixel à esquerda
            pixel_b = img.item(current_y-1, current_x, 0)
            pixel_g = img.item(current_y-1, current_x, 1)
            pixel_r = img.item(current_y-1, current_x, 2)

            # Verifica se tem uma borda

            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y, current_x + 1, 0)
                pixel_g = img.item(current_y, current_x + 1, 1)
                pixel_r = img.item(current_y, current_x + 1, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para o Sul
                    loc = location.SOUTH

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y + 1, current_x, 0)
                    pixel_g = img.item(current_y + 1, current_x, 1)
                    pixel_r = img.item(current_y + 1, current_x, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)
                            
                        # Vira à esquerda
                        loc = location.LEFT

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y, current_x - 1, 0)
                        pixel_g = img.item(current_y, current_x - 1, 1)
                        pixel_r = img.item(current_y, current_x - 1, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para a esquerda
                        else:
                            current_x += -1

                    # Senao anda ao Sul
                    else:

                        current_y += 1

                # Senao anda à direita
                else:

                    current_x += 1

            #Senao anda para o norte
            else:
                loc = location.NORTH
                current_y += -1

        elif loc == location.NORTH:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y, current_x-1, 0)
            pixel_g = img.item(current_y, current_x-1, 1)
            pixel_r = img.item(current_y, current_x-1, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y-1, current_x, 0)
                pixel_g = img.item(current_y-1, current_x, 1)
                pixel_r = img.item(current_y-1, current_x, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para a direita
                    loc = location.RIGHT

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y, current_x+1, 0)
                    pixel_g = img.item(current_y, current_x+1, 1)
                    pixel_r = img.item(current_y, current_x+1, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para o sul
                        loc = location.SOUTH

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y+1, current_x, 0)
                        pixel_g = img.item(current_y+1, current_x, 1)
                        pixel_r = img.item(current_y+1, current_x, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para o sul
                        else:
                            current_y += 1

                    # Senao anda para a direita
                    else:

                        current_x += 1

                # Senao anda para o norte
                else:

                    current_y += -1

            #Senão anda para a esquerda
            else:
                loc = location.LEFT
                current_x += -1


        elif loc == location.SOUTH:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y, current_x+1, 0)
            pixel_g = img.item(current_y, current_x+1, 1)
            pixel_r = img.item(current_y, current_x+1, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 255)
                    new_img.itemset((j, i, 1), 255)
                    new_img.itemset((j, i, 2), 255)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)

                # Olha o pixel à frente
                pixel_b = img.item(current_y+1, current_x, 0)
                pixel_g = img.item(current_y+1, current_x, 1)
                pixel_r = img.item(current_y+1, current_x, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para a esquerda
                    loc = location.LEFT

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y, current_x-1, 0)
                    pixel_g = img.item(current_y, current_x-1, 1)
                    pixel_r = img.item(current_y, current_x-1, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para o norte
                        loc = location.NORTH

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y-1, current_x, 0)
                        pixel_g = img.item(current_y-1, current_x, 1)
                        pixel_r = img.item(current_y-1, current_x, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)

                        # Senão anda para o norte
                        else:
                            current_y += -1

                    # Senao anda para a esquerda
                    else:

                        current_x += -1

                # Senao anda para o sul
                else:

                    current_y += 1

            #Senão anda para a direita
            else:
                loc = location.RIGHT
                current_x += 1




        elif loc == location.LEFT:
            # Olha o pixel à esquerda
            pixel_b = img.item(current_y+1, current_x, 0)
            pixel_g = img.item(current_y+1, current_x, 1)
            pixel_r = img.item(current_y+1, current_x, 2)

            #Verifica se tem uma borda
            if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                # Pinta o pixel à esquerda
                i = current_x
                j = current_y
                test_pixel = new_img.item(j, i, 0)
                while test_pixel == 0:
                    new_img.itemset((j, i, 0), 170)
                    new_img.itemset((j, i, 1), 0)
                    new_img.itemset((j, i, 2), 0)
                    j += 1
                    test_pixel = new_img.item(j, i, 0)
                    
                # Olha o pixel à frente
                pixel_b = img.item(current_y, current_x-1, 0)
                pixel_g = img.item(current_y, current_x-1, 1)
                pixel_r = img.item(current_y, current_x-1, 2)
                # Se tem uma borda
                if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                    # Pinta o pixel à frente
                    i = current_x
                    j = current_y
                    test_pixel = new_img.item(j, i, 0)
                    while test_pixel == 0:
                        new_img.itemset((j, i, 0), 170)
                        new_img.itemset((j, i, 1), 0)
                        new_img.itemset((j, i, 2), 0)
                        j += 1
                        test_pixel = new_img.item(j, i, 0)

                    # Vira para o norte
                    loc = location.NORTH

                    # Olha o pixel à frente
                    pixel_b = img.item(current_y-1, current_x, 0)
                    pixel_g = img.item(current_y-1, current_x, 1)
                    pixel_r = img.item(current_y-1, current_x, 2)

                    # Se tem uma borda
                    if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                        # Pinta o pixel à frente
                        i = current_x
                        j = current_y
                        test_pixel = new_img.item(j, i, 0)
                        while test_pixel == 0:
                            new_img.itemset((j, i, 0), 170)
                            new_img.itemset((j, i, 1), 0)
                            new_img.itemset((j, i, 2), 0)
                            j += 1
                            test_pixel = new_img.item(j, i, 0)

                        # Vira para a direita
                        loc = location.RIGHT

                        # Olha o pixel à frente
                        pixel_b = img.item(current_y, current_x+1, 0)
                        pixel_g = img.item(current_y, current_x+1, 1)
                        pixel_r = img.item(current_y, current_x+1, 2)

                        # Se tem uma borda
                        if pixel_b < 20 and pixel_g < 20 and pixel_g < 20:

                            # Pinta a borda
                            i = current_x
                            j = current_y
                            test_pixel = new_img.item(j, i, 0)
                            while test_pixel == 0:
                                new_img.itemset((j, i, 0), 170)
                                new_img.itemset((j, i, 1), 0)
                                new_img.itemset((j, i, 2), 0)
                                j += 1
                                test_pixel = new_img.item(j, i, 0)
                                
                        # Senão anda para o direita
                        else:
                            current_x += 1

                    # Senao anda para o norte
                    else:

                        current_y += -1

                # Senao anda para esquerda
                else:

                    current_x += -1

            #Senão anda para o sul
            else:
                loc = location.SOUTH
                current_y += 1
    print("Bordas de " + str(entry) + " calculadas")
    cv2.imwrite(str(entry)+"_preenchido", new_img)
