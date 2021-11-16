# -*- coding: utf-8 -*-
#!/usr/bin/env python3

################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#       Script desenvolvido por Alex Borges, amborges@inf.ufpel.edu.br.        #
#                  Grupo de Pesquisa Video Technology Research Group -- ViTech #
#                                     Universidade Federal de Pelotas -- UFPel #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
# script de configuração compatível com o arquivo main.py versão 1.1           #
################################################################################

################################################################################
#                     ARQUIVO DE CONFIGURAÇÃO DEDICADO PARA O                  #
################################################################################
#                                                                              #
#                                                                              #
#                          #####  #       #    ##                              #
#                          #   #   #     #   #  #                              #
#                          #####    #   #       #                              #
#                          #   #     # #        #                              #
#                          #   #      #         #                              #
#                                                                              #
#                                                                              #
################################################################################

################################################################################
###                            Configurações Gerais                          ###
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -###
### Aqui tu prepara as condições das simulações que queres executar para os  ###
### teus experimentos. Apesar de estar preparado inicialmente para o AV1,    ###
### com o software libaom, modificações para outros codificadores é          ###
### relativamente simples. Basicamente é necessário modificar algumas pastas ###
### e nomes. Ao longo deste arquivo, vou comentando algumas funcionalidades. ###
################################################################################

#################################
## Ativação de Funcionalidades ##
#################################

# Precisa baixar o libaom?
import os
DOWNLOAD = False

# Se precisar que o download do libaom seja regredido para alguma versão passada
# então modifique o texto abaixo para a versão requerida. Utilize somente os
# seis primeiros caracteres da versão, por exemplo 'df1c60'
DOWNGRADE_TO = ''

# Precisa compilar o libaom?
COMPILE = False

# Quer realizar somente uma única simulação, para ver alguma coisa específica?
TESTE = False

# É para executar de fato o experimento, com todas as simulações possíveis?
EXECUTE = True

# Quer que mostre na tela o estado geral das simulações?
# Caso opte por False, o arquivo de log ainda será gerado.
VERBOSE = True

######################################
## Parâmetros Gerais das Simulações ##
######################################

# Lista de núcleos que podem ser utilizados, lembre sempre de deixar pelo menos
# um único núcleo para o sistema operacional.
ALLOWED_CORES = [1]
# ALLOWED_CORES = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

# Lista de CQs a serem utilizados, deixe descomentado o que tu preferir
# CQ_LIST = [20] #test
CQ_LIST = [55, 43, 32, 20]  # short list
# CQ_LIST = [20, 24, 28, 32, 36, 39, 43, 47, 51, 55] #full list

# Parâmetros extras que podem ser incluídos ao codificador.
# Este é um atributo que permite criar várias simulações onde há apenas a inclusão
# de um ou mais parâmetros ao codificador, além daqueles parâmetros padrões que
# devem estar inclusos (que eu chamo de codificação âncora). Se tu deixar a lista
# vazia, então somente uma única simulação será realizada com aquele vídeo naquele
# CQ. Caso tu adicionar algo, então esse algo será uma simulação a mais que será
# realizada. Cada nova variação de simulação será identificada nos arquivos de saída.
# POR FAVOR, lembre de adicionar um espaço entre as aspas e o parâmetro em si. Só
# pra facilitar o meu trabalho durante o código. Sim, foi preguiça.
# Exemplos:
# EXTRA_PARAMS = [] # sem parâmetros extras, 1 conjunto de experimento
# EXTRA_PARAMS = [' --enable-rect-partitions=0'] # UM parâmetro extra, 2 conjuntos de experimentos
# EXTRA_PARAMS = [' --enable-rect-partitions=0', ' --min-partition-size=16 --max-partition-size=64'] # DOIS parâmetros, 3 conjuntos
EXTRA_PARAMS = []

############################
## Configuração do SCRIPT ##
############################

# Quantidade de quadros a ser executado (frames to be executed)
# Se deixar com valor negativo, então o vídeo inteiro será codificado
FTBE = 2


# Opção que define se deve considerar limite por tempo em segundos (enable limit for seconds)
# em vez de quantidade de quadros.
# Alan
ELFS = True

# Quantidade de segundos a serem executados (seconds to be executed)
# independentemente da quantidade de quadros definido
# Se o valor for maior que zero o FTBE será desconsiderado
# Alan
TEMP_SEG = 1

# tempo de espera para verificar os processos em pilha (em segundos)
# Quanto mais curto, mais vezes ele faz uma leitura dos processos
# em um mesmo período de tempo. Tente ser razoável, por exemplo,
# tu vai executar somente vídeos UHD4K, sabe-se que eles levam pelo
# menos uns três dias (chegando a sete em alguns casos) para codificar.
# Neste caso, não faz o menor sentido verificar o processo a cada 30seg.
# Para esse caso específico, uma vez por dia tá bom (86400). Agora
# se tu vai usar o setup completo de vídeos, uma vez a cada uma hora
# tá de bom tamanho (3600)
WAITING_TIME = 3600

# Número máximo de núcleos que podem ser utilizados simultaneamente
# Em geral, se tu selecionou os cores disponíveis, é pq eles podem
# ser utilizados. Acaso tiveres alguma restrição, modificar aqui.
# O detalhe é que o computador não utilizará todos os núcleos
# anotados em ALLOWED_CORES
MAX_CORES = len(ALLOWED_CORES)

# nome do codificador. Se houver alguma mudança, mude aqui
CODEC_NAME = 'aomenc'

# tipo de extensão do vídeo. PREFERENCIALMENTE Y4M.
# MAS caso tu preferir utilizar YUV, modifique a função GENERATE_COMMAND
# para incluir as informações de altura, largura, bit-depth, subsample e fps.
# Alan - Sem uso agora ->VIDEO_EXTENSION = '.yuv'

##########################
## Definição das Pastas ##
##########################

# caminho da pasta de compilação do libaom
# o /bin/ no final é criado automaticamente pelo script.
# é de lá que ele vai compilar e manter os executáveis
CODEC_PATH = '/home/icaro/av1_pesquisa/aom/build_d/'
# CODEC_PATH = '/home/simulacoes_av1/av1_pesquisa/aom/build_debug/'

# caminhos das pastas dos vídeos separados por resolução
VIDEOS_PATH = {
    '240p': '/home/icaro/Videos/vvc/',
    '360p': '/home/icaro/Videos/vvc/',
    '480p': '/home/icaro/Videos/vvc/',
    '720p': '/home/icaro/Videos/vvc/',
    '1080p': '/home/icaro/Videos/vvc/',
    '1080pscc': '/home/icaro/Videos/vvc/',
    'uhd4k': '/home/icaro/Videos/vvc/'
}
# VIDEOS_PATH = {
# 	'240p': '/home/data/YUV/',
# 	'360p': '/home/data/YUV/',
# 	'480p': '/home/data/YUV/',
# 	'720p': '/home/data/YUV/',
# 	'1080p': '/home/data/YUV/',
# 	'1080pscc': '/home/data/YUV/',
# 	'uhd4k': '/home/data/YUV/'
# }

# Lista de vídeos a serem utilizados
# Cada linha é composta por uma resolução (vide acima) e o nome do vídeo
# Também incluí o SI-TI do vídeo, e marquei aqueles que eu considerdo
# recomendados para os nossos experimentos no ViTech.
# Descomente os vídeos que queres utilizar
VIDEOS_LIST = [
    # CLASS_D
    #['240p', 'BlowingBubbles_416x240_50.yuv'],
    ['240p', 'BQSquare_416x240_60.yuv'],

    # CLASS_C
    #['480p', 'BQMall_832x480_60.yuv'],
    ['480p', 'RaceHorsesC_832x480_30.yuv'],

    # CLASS_B
    #['1080p', 'Cactus_1920x1080_50.yuv'],
    ['1080p', 'Kimono_1920x1080_24.yuv'],

    # CLASS_A
]


############################# [ [ [ A  T  E  N  Ç  Ã  O ] ] ] ########################################
#       Aqui se encontram funções que poderão sofrer mudanças. Deve-se alterar o que for preciso     #
#           para que a linha de comando seja adequada ao codificador que se está utilizando          #
######################################################################################################

# entradas vindas da classe LIST_OF_EXPERIMENTS, esses valores não são alteráveis.
# todos os valores são do tipo texto.
#   core, número do núcleo em que o experimento vai ser executado
#   cq, valor de quantização (CQ)
#   folder, nome da pasta em que o experimento será executado
#   video_path, caminho completo do vídeo que será codificado
# Alan - fps, altura e largura
def GENERATE_COMMAND(core, cq, folder, video_path, extra_param='', fps=0, largura=0, altura=0):

    # criando cada parte da linha de comando. Lembrar do espaçamento entre os parâmetros

    # nome da configuração extra_param, se existir
    ep_name = ''
    if extra_param != '':
        ep_name = "_set_" + \
            extra_param.replace(' ', '').replace('-', '').replace('=', '')

    # definindo aonde a codificação será executada
    cd_param = 'cd ' + folder + ' & '

    # definindo em qual núcleo o experimento será executado
    taskset_param = 'taskset -c ' + core + ' '

    # definindo o limite de frames a ser executado
    limit_param = ''

    # Alan -->
    # Limite por quadros ou tempo em segundos
    if (not ELFS):
        limite = FTBE
    else:
        limite = int(TEMP_SEG) * int(fps)
    if(limite > 0):
        limit_param = ' --limit=' + str(limite)

    # Dimensões do vídeo
    if (len(altura) > 2 and len(largura) > 2):
        dimensao = ' --width=' + str(largura) + ' --height=' + str(altura)
    # Alan <--

    # definindo a quantização
    # A princípio, se ao invés do CQ, for utilizar bitrate, basta trocar a linha para:
    #cq_param = ' --end-usage=vbr --target-bitrate=' + cq
    cq_param = ' --end-usage=q --cq-level=' + cq

    # definindo o arquivo de saída do vídeo codificado
    webm_param = ' -o ' + folder + '/cq_' + cq + '/webm/coded' + ep_name + '.webm'

    # definindo aonde que ficará salvo as saídas do codificador
    output_filename = folder + '/cq_' + cq + '/log/out' + ep_name + '.log'
    output_param = ' > ' + output_filename + ' 2>&1'

    # definindo outras configurações gerais para o libaom
    fixed_param = ' --verbose --psnr --frame-parallel=0 --tile-columns=0 --passes=2 --cpu-used=0 --threads=1 --kf-min-dist=1000 --kf-max-dist=1000 --lag-in-frames=19'

    # Criando a linha de comando completa
    codec_command = cd_param
    codec_command += taskset_param
    codec_command += CODEC_PATH + CODEC_NAME
    codec_command += fixed_param
    codec_command += limit_param
    codec_command += cq_param
    codec_command += dimensao
    # normalmente vazio, mas pode conter parâmetros presente em EXTRA_PARAMS
    codec_command += extra_param
    codec_command += webm_param
    codec_command += ' ' + video_path
    codec_command += output_param + ' &'
    # o & comercial no final serve para colocar o processo em segundo plano!

    # retornando a linha de comando e o arquivo de saída
    return codec_command, output_filename


# A seguinte função lê o arquivo de log e retorna os três valores relevantes de cada arquivo
# entrada, o nome do arquivo que se deseja ler
# saída, o PSNR-Y, o bitrate e o tempo de execução. Todas do tipo float
def get_psnr_bitrate_time(from_file):
    # abro o arquivo obtido do libaom
    f = open(from_file)
    # preciso da última linha, mas tenho que passar por todo o arquivo
    for lst_line in f:
        # pass
        print(lst_line)
        if "(Overall/Avg/Y/U/V)" in lst_line:
            break
    f.close()
    # separo a linha em palavras
    words = lst_line.split(' ')
    # removo os indexes que não contêm palavras
    words = list(filter(lambda a: len(a) > 0, words))
    # idx = o que aparece
    # 0  =  Stream
    # 1  =  0
    # 2  =  PSNR
    # 3  =  (Overall/Avg/Y/U/V)
    # 4  =  44.452
    # 5  =  45.206
    # 6  =  44.286
    # 7  =  48.271
    # 8  =  48.832
    # 9  =  4193982
    # 10  =  bps
    # 11  =  27382
    # 12  =  ms\n

    # O que me interessa são o PSNR-Y (6), bitrate (9) e o tempo (11)
    psnr_y = float(words[6])
    bitrate = float(words[9])
    time = float(words[11])
    return psnr_y, bitrate, time


# Função que permite baixar o libaom
# pego somente o caminho do aom, sem o bin/


def DO_DOWNLOAD():
    codec_path = CODEC_PATH[:-4]
    if(os.path.exists(codec_path)):
        # se a pasta já existe, apagar tudo
        os.system('rm -rf ' + codec_path)

    # faz download do libaom e coloca na pasta desejada
    git_command = 'git clone https://aomedia.googlesource.com/aom ' + codec_path

    # caso deseja fazer downgrade...
    if DOWNGRADE_TO != '':
        git_command += ' && cd ' + codec_path + ' && git reset --hard ' + DOWNGRADE_TO

    # executa o git
    os.system(git_command)


# Função que compila o libaom
# O código já adapta para possíveis versões diferentes de sistema operacional
def DO_COMPILE(os_version):
    # se precisar compilar o libaom, então COMPILA
    if(os.path.exists(CODEC_PATH)):
        # se a pasta já existe, apagar tudo pra deixar uma compilação limpa
        os.system('rm -rf ' + CODEC_PATH)
    os.system('mkdir ' + CODEC_PATH)

    if os_version == 18.04:
        # Em algumas máquinas, dá pra rodar a linha de baixo. O libaom fica especializado
        cmake_command = 'cd ' + CODEC_PATH + ' && cmake ..'
    elif os_version > 18.04:
        # Mas na maioria não, daí tem que compilar de forma genérica:
        cmake_command = 'cd ' + CODEC_PATH + ' && cmake -DAOM_TARGET_CPU=generic ..'
    else:
        # Em caso de ubuntu mais velho, utilizar a seguinte chamada:
        cmake_command = 'cd ' + CODEC_PATH + \
            ' && cmake -DAOM_TARGET_CPU=generic -DENABLE_DOCS=0 ..'
    make_command = 'cd ' + CODEC_PATH + ' && make'
    os.system(cmake_command)
    os.system(make_command)
