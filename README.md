# IC-2018-analise-de-textura
Avaliação de agregados minerais quanto ao estado de alteração por meio de análise de textura de imagens digitais
Os arquivos "script_roi_32x32.py", "script_roi_48x48.py" e "script_roi_64x64.py" geram um arquivo ARFF contendo valores das entropias dos canais R, G, B, etc analisando uma região de interesse de tamanho 32x32, 48x48 e 64x64, respectivamente, das imagens da pasta "granito".
O arquivo "script_pedra_inteira.py" gera um arquivo ARFF com as entropias de uma pedra inteira, mas para isso é necessário o pré-processamento das imagens com os arquivos "script_borders.py" e "script_preenchido.py".
