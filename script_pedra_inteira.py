#!python3
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math

with open("entropia_inteira","w") as f:
    f.write("@relation Entropia\n@attribute b numeric\n@attribute g numeric\n@attribute r numeric\n@attribute gray numeric\n@attribute lbp numeric\n@attribute bg numeric\n@attribute gr numeric\n@attribute br numeric\n@attribute tipo {alterado, naoAlterado}\n\n@data\n")
    #Altera a pasta de trabalho e cria uma lista com todas as imagens
    os.chdir('granito/nao_alterado/')
    lista_imagens = sorted(os.listdir('.'))

    #Loop de leitura de todas as imagens na pasta
    for entry in lista_imagens:

        #print(entry)
        nome = str(entry)
        if nome.find("borders") >= 0:
            continue
        if nome.find("preenchido") >= 0:
            continue

        #Leitura da imagem
        img = cv2.imread(entry, cv2.IMREAD_COLOR)
        compare_img = cv2.imread(str(entry) + "_preenchido", 0) #Abre em escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bList = list()
        gList = list()
        rList = list()
        grayList = list()
        bgList = list()
        grList = list()
        brList = list()
        lbp = list()

        y, x, z = img.shape

        for i in range(256):

            bList.append(0)
            gList.append(0)
            rList.append(0)
            grayList.append(0)
            bgList.append(0)
            grList.append(0)
            brList.append(0)
            lbp.append(0)
        total_b = 0
        total_pixel = 0
        for i in range(y):
            for j in range(x):

                #Se o pixel na imagem de comparação for preto deve ser ignorado
                value_compare = compare_img.item(i,j)
                if value_compare == 0:
                    total_b += 1
                    continue
                total_pixel += 1
                valueB = img.item(i,j,0)
                valueG = img.item(i,j,1)
                valueR = img.item(i,j,2)
                valueGray = gray.item(i,j)
                bList[valueB] = bList[valueB] + 1
                gList[valueG] = gList[valueG] + 1
                rList[valueR] = rList[valueR] + 1
                grayList[valueGray] = rList[valueGray] + 1
                bgList[(valueB+valueG) // 2] = bgList[(valueB+valueG) // 2] + 1
                grList[(valueR+valueG) // 2] = grList[(valueR+valueG) // 2] + 1
                brList[(valueB+valueR) // 2] = brList[(valueB+valueR) // 2] + 1
        size = total_pixel
        print(size)
        print(total_b)
        print(total_pixel)
        bEntropy = 0
        gEntropy = 0
        rEntropy = 0
        grayEntropy = 0
        bgEntropy = 0
        grEntropy = 0
        brEntropy = 0
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

        #Entropia do canal Azul + Verde
        for i in bgList:
            if i == 0:
                continue
            else:
                bgEntropy = bgEntropy + (i/size)*(math.log2(size/i))


        #Entropia do canal Verde + Vermelho
        for i in grList:
            if i == 0:
                continue
            else:
                grEntropy = grEntropy + (i/size)*(math.log2(size/i))


        #Entropia do canal Azul + Vermelho
        for i in brList:
            if i == 0:
                continue
            else:
                brEntropy = brEntropy + (i/size)*(math.log2(size/i))

        ##### LBP #####
        (h,w) = gray.shape[:2]

       # Quadradinhos em X
        q_x = w // 3

        # Quadradinhos em Y
        q_y = h // 3

        #Total de quadrados para o LBP
        q_total = q_x * q_y

        outofrange = False
        for i in range(q_y):
            for j in range(q_x):
                if(compare_img.item(i*3, j*3) ==  0):
                    outofrange = True
                if(compare_img.item(1 + i*3, j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, 1 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(1 + i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(i*3, 1 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(1 + i*3, 1 + j*3) == 0):
                    outofrange = True

                if(outofrange == True):
                    q_total = q_total - 1
                    continue

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
        f.write(str(bEntropy) +", ")
        print("Entropia verde: " + str(gEntropy))
        f.write(str(gEntropy) + ", ")
        print("Entropia vermelho: " + str(rEntropy))
        f.write(str(rEntropy) + ", ")
        print("Entropia cinza: " + str(grayEntropy))
        f.write(str(grayEntropy) + ", ")
        print("Entropia LBP: " + str(lbpEntropy))
        f.write(str(lbpEntropy) + ", ")
        print("Entropia Azul + Verde: " + str(bgEntropy))
        f.write(str(bgEntropy) + ", ")
        print("Entropia Verde + Vermelho: " + str(grEntropy))
        f.write(str(grEntropy) + ", ")
        print("Entropia Azul + Vermelho: " + str(brEntropy))
        f.write(str(brEntropy) + ", ")
        f.write("naoAlterado\n")
        print()
        #cv2.imshow('image',roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




    #Altera a pasta de trabalho e cria uma lista com todas as imagens
    os.chdir('../alterado/')
    lista_imagens = sorted(os.listdir('.'))

    #Loop de leitura de todas as imagens na pasta
    for entry in lista_imagens:

        #print(entry)
        nome = str(entry)
        if nome.find("borders") >= 0:
            continue
        if nome.find("preenchido") >= 0:
            continue

        #Leitura da imagem
        img = cv2.imread(entry, cv2.IMREAD_COLOR)
        compare_img = cv2.imread(str(entry) + "_preenchido", 0) #Abre em escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bList = list()
        gList = list()
        rList = list()
        grayList = list()
        bgList = list()
        grList = list()
        brList = list()
        lbp = list()

        y, x, z = img.shape

        for i in range(256):

            bList.append(0)
            gList.append(0)
            rList.append(0)
            grayList.append(0)
            bgList.append(0)
            grList.append(0)
            brList.append(0)
            lbp.append(0)
        total_b = 0
        total_pixel = 0
        for i in range(y):
            for j in range(x):

                #Se o pixel na imagem de comparação for preto deve ser ignorado
                value_compare = compare_img.item(i,j)
                if value_compare == 0:
                    total_b += 1
                    continue
                total_pixel += 1
                valueB = img.item(i,j,0)
                valueG = img.item(i,j,1)
                valueR = img.item(i,j,2)
                valueGray = gray.item(i,j)
                bList[valueB] = bList[valueB] + 1
                gList[valueG] = gList[valueG] + 1
                rList[valueR] = rList[valueR] + 1
                grayList[valueGray] = rList[valueGray] + 1
                bgList[(valueB+valueG) // 2] = bgList[(valueB+valueG) // 2] + 1
                grList[(valueR+valueG) // 2] = grList[(valueR+valueG) // 2] + 1
                brList[(valueB+valueR) // 2] = brList[(valueB+valueR) // 2] + 1
        size = total_pixel
        print(size)
        print(total_b)
        print(total_pixel)
        bEntropy = 0
        gEntropy = 0
        rEntropy = 0
        grayEntropy = 0
        bgEntropy = 0
        grEntropy = 0
        brEntropy = 0
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

        #Entropia do canal Azul + Verde
        for i in bgList:
            if i == 0:
                continue
            else:
                bgEntropy = bgEntropy + (i/size)*(math.log2(size/i))


        #Entropia do canal Verde + Vermelho
        for i in grList:
            if i == 0:
                continue
            else:
                grEntropy = grEntropy + (i/size)*(math.log2(size/i))


        #Entropia do canal Azul + Vermelho
        for i in brList:
            if i == 0:
                continue
            else:
                brEntropy = brEntropy + (i/size)*(math.log2(size/i))

        ##### LBP #####
        (h,w) = gray.shape[:2]

       # Quadradinhos em X
        q_x = w // 3

        # Quadradinhos em Y
        q_y = h // 3

        #Total de quadrados para o LBP
        q_total = q_x * q_y

        outofrange = False
        for i in range(q_y):
            for j in range(q_x):
                if(compare_img.item(i*3, j*3) ==  0):
                    outofrange = True
                if(compare_img.item(1 + i*3, j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, 1 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(2 + i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(1 + i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(i*3, 2 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(i*3, 1 + j*3) == 0):
                    outofrange = True
                if(compare_img.item(1 + i*3, 1 + j*3) == 0):
                    outofrange = True

                if(outofrange == True):
                    q_total = q_total - 1
                    continue

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
        f.write(str(bEntropy) +", ")
        print("Entropia verde: " + str(gEntropy))
        f.write(str(gEntropy) + ", ")
        print("Entropia vermelho: " + str(rEntropy))
        f.write(str(rEntropy) + ", ")
        print("Entropia cinza: " + str(grayEntropy))
        f.write(str(grayEntropy) + ", ")
        print("Entropia LBP: " + str(lbpEntropy))
        f.write(str(lbpEntropy) + ", ")
        print("Entropia Azul + Verde: " + str(bgEntropy))
        f.write(str(bgEntropy) + ", ")
        print("Entropia Verde + Vermelho: " + str(grEntropy))
        f.write(str(grEntropy) + ", ")
        print("Entropia Azul + Vermelho: " + str(brEntropy))
        f.write(str(brEntropy) + ", ")
        f.write("alterado\n")
        print()
        #cv2.imshow('image',roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
