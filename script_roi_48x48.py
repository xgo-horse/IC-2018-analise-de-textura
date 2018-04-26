#!python3
"""
script_roi_48x48.py gera um arquivo arff contendo as entropias analizando uma area de 48x48.
As entropias calculadas são:
Canal B
Canal G
Canal R
Cinza
LBP
Canal B + G
Canal G + R
Canal B + R

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math

with open("entropia48x48","w") as f:
    f.write("@relation Entropia\n@attribute b numeric\n@attribute g numeric\n@attribute r numeric\n@attribute gray numeric\n@attribute lbp numeric\n@attribute bg numeric\n@attribute gr numeric\n@attribute br numeric\n@attribute tipo {alterado, naoAlterado}\n\n@data\n")
    #Altera a pasta de trabalho e cria uma lista com todas as imagens
    os.chdir('granito/granito-nao alterado/')
    lista_imagens = sorted(os.listdir('.'))

    #Loop de leitura de todas as imagens na pasta
    for entry in lista_imagens:
        
        #print(entry)
        if entry.find("borders") >= 0:
            continue
        if entry.find("preenchido") >= 0:
            continue
                
        #Leitura da imagem
        img = cv2.imread(entry, cv2.IMREAD_COLOR)
        
        #Pega o total X e Y da imagem e calcula o ponto central
        x,y,z = img.shape
        middlex = x//2
        middley = y//2

        #Recorta um quadrado de 48x48 tendo como meio o pixel central
        roi = img[middlex-24:middlex+24,middley-24:middley+24]

        #Cria uma imagem em escala de cinza
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        bList = list()
        gList = list()
        rList = list()
        grayList = list()
        bgList = list()
        grList = list()
        brList = list()
        lbp = list()

        #print(roi.item(0,0,1))
        
        for i in range(256):

            bList.append(0)    
            gList.append(0)
            rList.append(0)
            grayList.append(0)
            bgList.append(0)
            grList.append(0)
            brList.append(0)
            lbp.append(0)


        for i in range(48):
            for j in range(48):
                valueB = roi.item(i,j,0)
                valueG = roi.item(i,j,1)
                valueR = roi.item(i,j,2)
                valueGray = gray.item(i,j)
                bList[valueB] = bList[valueB] + 1
                gList[valueG] = gList[valueG] + 1
                rList[valueR] = rList[valueR] + 1
                grayList[valueGray] = rList[valueGray] + 1
                bgList[(valueB + valueG) // 2] += 1
                grList[(valueG + valueR) // 2] += 1
                brList[(valueB + valueR) // 2] += 1
        size = roi.size
        bEntropy = 0
        gEntropy = 0
        rEntropy = 0
        grayEntropy = 0
        bgEntropy = 0
        grEntropy = 0
        brEntropy = 0
        lbpEntropy = 0
        #Entropia do canal Azul
        for i in bList:
            if i == 0:
                continue
            else:
                bEntropy = bEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Verde
        for i in gList:
            if i == 0:
                continue
            else:
                gEntropy = gEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Vermelho
        for i in rList:
            if i == 0:
                continue
            else:
                rEntropy = rEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Cinza
        for i in grayList:
            if i == 0:
                continue
            else:
                grayEntropy = grayEntropy + (i/size)*(math.log2(size/i))

        #Entropia do Azul + Verde
        for i in bgList:
            if i == 0:
                continue
            else:
                bgEntropy += (i/size)*math.log2(size/i)

        #Entropia do Verde + Vermelho
        for i in grList:
            if i == 0:
                continue
            else:
                grEntropy += (i/size)*math.log2(size/i)

        #Entropia do Azul + Vermelho
        for i in brList:
            if i == 0:
                continue
            else:
                brEntropy += (i/size)*math.log2(size/i)

        ##### LBP #####
        (h,w) = gray.shape[:2]

        # Quadradinhos em X
        q_x = w // 3

        # Quadradinhos em Y
        q_y = h // 3

        #Total de quadrados para o LBP
        q_total = q_x * q_y

        
        for i in range(q_x):
            for j in range(q_y):
                a_lbp = gray.item(i*3, j*3)
                b_lbp = gray.item(1 + i*3, j*3)
                c_lbp = gray.item(2 + i*3, j*3)
                d_lbp = gray.item(2 + i*3, 1 + j*3)
                e_lbp = gray.item(2 + i*3, 2 + j*3)
                f_lbp = gray.item(1 + i*3, 2 + j*3)
                g_lbp = gray.item(i*3, 2 + j*3)
                h_lbp = gray.item(i*3, 1 + j*3)
                center_lbp = gray.item(1 + i*3, 1 + j*3)

            value = 0
            if a_lbp > center_lbp:
                value += 1
            if b_lbp > center_lbp:
                value += 2
            if c_lbp > center_lbp:
                value += 4
            if d_lbp > center_lbp:
                value += 8
            if e_lbp > center_lbp:
                value += 16
            if f_lbp > center_lbp:
                value += 32
            if g_lbp > center_lbp:
                value += 64
            if h_lbp > center_lbp:
                value += 128
            lbp[value] += 1   
        lbpEntropy = 0
        lbpSize = q_total
        
        for i in lbp:
            if i == 0:
                continue
            else:
                lbpEntropy = lbpEntropy + (i/lbpSize)*(math.log2(lbpSize/i))
        #####      
                
        
            
        print("Entropia azul: " + str(bEntropy))
        f.write(str(bEntropy) +",	 ")
        print("Entropia verde: " + str(gEntropy))
        f.write(str(gEntropy) + ",	 ")
        print("Entropia vermelho: " + str(rEntropy))
        f.write(str(rEntropy) + ",	 ")
        print("Entropia cinza: " + str(grayEntropy))
        f.write(str(grayEntropy) + ",	 ")
        print("Entropia LBP: " + str(lbpEntropy))
        f.write(str(lbpEntropy) + ",	 ")
        print("Entropia Azul + Verde: " + str(bgEntropy))
        f.write(str(bgEntropy) + ",	 ")
        print("Entropia Verde + Vermelho: " + str(grEntropy))
        f.write(str(grEntropy) + ",	 ")
        print("Entropia Azul + Vermelho: " + str(brEntropy))
        f.write(str(brEntropy) + ",	 ")
        f.write("naoAlterado\n")
        print()
        #cv2.imshow('image',roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #Altera a pasta de trabalho para a pasta que contem as imagens alteradas
    os.chdir('../granito-alterado')
    lista_imagens = sorted(os.listdir('.'))

    for entry in lista_imagens:

        if entry.find("borders") >= 0:
            continue
        if entry.find("preenchido") >= 0:
            continue
        
 
        img = cv2.imread(entry, cv2.IMREAD_COLOR)

        #Pega o total X e Y da imagem e calcula o ponto central
        x,y,z = img.shape
        middlex = x//2
        middley = y//2

        #Recorta um quadrado de 48x48 tendo como meio o pixel central
        roi = img[middlex-24:middlex+24,middley-24:middley+24]

        #Cria uma imagem em escala de cinza
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        bList = list()
        gList = list()
        rList = list()
        grayList = list()
        bgList = list()
        grList = list()
        brList = list()
        lbp = list()
        
        #print(roi.item(0,0,1))
        
        for i in range(256):

            bList.append(0)    
            gList.append(0)
            rList.append(0)
            grayList.append(0)
            bgList.append(0)
            grList.append(0)
            brList.append(0)
            lbp.append(0)


        for i in range(48):
            for j in range(48):
                valueB = roi.item(i,j,0)
                valueG = roi.item(i,j,1)
                valueR = roi.item(i,j,2)
                valueGray = gray.item(i,j)
                bList[valueB] = bList[valueB] + 1
                gList[valueG] = gList[valueG] + 1
                rList[valueR] = rList[valueR] + 1
                grayList[valueGray] = rList[valueGray] + 1
                bgList[(valueB + valueG) // 2] += 1
                grList[(valueG + valueR) // 2] += 1
                brList[(valueB + valueR) // 2] += 1
                
        size = roi.size
        bEntropy = 0
        gEntropy = 0
        rEntropy = 0
        grayEntropy = 0
        bgEntropy = 0
        grEntropy = 0
        brEntropy = 0
        lbpEntropy = 0
        #Entropia do canal Azul
        for i in bList:
            if i == 0:
                continue
            else:
                bEntropy = bEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Verde
        for i in gList:
            if i == 0:
                continue
            else:
                gEntropy = gEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Vermelho
        for i in rList:
            if i == 0:
                continue
            else:
                rEntropy = rEntropy + (i/size)*(math.log2(size/i))

        #Entropia do canal Cinza
        for i in grayList:
            if i == 0:
                continue
            else:
                grayEntropy = grayEntropy + (i/size)*(math.log2(size/i))

        #Entropia do Azul + Verde
        for i in bgList:
            if i == 0:
                continue
            else:
                bgEntropy += (i/size)*math.log2(size/i)

        #Entropia do Verde + Vermelho
        for i in grList:
            if i == 0:
                continue
            else:
                grEntropy += (i/size)*math.log2(size/i)

        #Entropia do Azul + Vermelho
        for i in brList:
            if i == 0:
                continue
            else:
                brEntropy += (i/size)*math.log2(size/i)

        ##### LBP #####
        (h,w) = gray.shape[:2]

        # Quadradinhos em X
        q_x = w // 3

        # Quadradinhos em Y
        q_y = h // 3

        #Total de quadrados para o LBP
        q_total = q_x * q_y

        
        for i in range(q_x):
            for j in range(q_y):
                a_lbp = gray.item(i*3, j*3)
                b_lbp = gray.item(1 + i*3, j*3)
                c_lbp = gray.item(2 + i*3, j*3)
                d_lbp = gray.item(2 + i*3, 1 + j*3)
                e_lbp = gray.item(2 + i*3, 2 + j*3)
                f_lbp = gray.item(1 + i*3, 2 + j*3)
                g_lbp = gray.item(i*3, 2 + j*3)
                h_lbp = gray.item(i*3, 1 + j*3)
                center_lbp = gray.item(1 + i*3, 1 + j*3)

            value = 0
            if a_lbp > center_lbp:
                value += 1
            if b_lbp > center_lbp:
                value += 2
            if c_lbp > center_lbp:
                value += 4
            if d_lbp > center_lbp:
                value += 8
            if e_lbp > center_lbp:
                value += 16
            if f_lbp > center_lbp:
                value += 32
            if g_lbp > center_lbp:
                value += 64
            if h_lbp > center_lbp:
                value += 128
            lbp[value] += 1   
        lbpEntropy = 0
        lbpSize = q_total
        
        for i in lbp:
            if i == 0:
                continue
            else:
                lbpEntropy = lbpEntropy + (i/lbpSize)*(math.log2(lbpSize/i))
        #####      
 

        print("Entropia alterado azul: " + str(bEntropy))
        f.write(str(bEntropy) +",	 ")
        print("Entropia alterado verde: " + str(gEntropy))
        f.write(str(gEntropy) + ",	 ")
        print("Entropia alterado vermelho: " + str(rEntropy))
        f.write(str(rEntropy) + ",	 ")
        print("Entropia alterado cinza: " + str(grayEntropy))
        f.write(str(grayEntropy) + ",	 ")
        print("Entropia LBP: " + str(lbpEntropy))
        f.write(str(lbpEntropy) + ",	 ")
        print("Entropia Azul + Verde: " + str(bgEntropy))
        f.write(str(bgEntropy) + ",	 ")
        print("Entropia Verde + Vermelho: " + str(grEntropy))
        f.write(str(grEntropy) + ",	 ")
        print("Entropia Azul + Vermelho: " + str(brEntropy))
        f.write(str(brEntropy) + ",	 ")
        f.write("alterado\n")
        print()
        #cv2.imshow('image',roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
