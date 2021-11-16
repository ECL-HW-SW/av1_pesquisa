# -*- coding: utf-8 -*-
#!/usr/bin/env python3

################################################################################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#       Script desenvolvido por Alex Borges, amborges@inf.ufpel.edu.br.        #
#                  Grupo de Pesquisa Video Technology Research Group -- ViTech #
#                                     Universidade Federal de Pelotas -- UFPel #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                                                                              #
#                                            Versão 1.1, 19 de Janeiro de 2021 #
#                                                                              #
# Melhorias em relação à versão 1.0:                                           #
# - Lê os arquivos de saída do libaom para capturar valores de psnr, bitrate e #
# tempo;                                                                       #
# - Exporta os valores capturados dos arquivos de saída para um csv;           #
# - Gera o valor de BD-rate entre duas codificações;                           #
# - Gera gráfico da curva de BD-rate;                                          #
# - Calcula a razão de tempo entre duas codificações;                          #
# - Exporta os valores de BD-rate e a razão do tempo para um csv;              #
# - Compilação do libaom foi adequada para versões diferentes do Ubuntu;       #
# - Funções dependentes de codificador foram extraídos de main.py e enviados   #
# para CONFIGURATIONS.py;                                                      #
# - Adicionei uma função extra para exportar todos os print do código para um  #
# arquivo de log externo;                                                      #
# - Adicionei controle de textos no terminal (opção verbose).                  #
#                                                                              #
# Problemas conhecidos:                                                        #
# - Avisos de descontinuidade de funções do matplotlib.                        #
#      Solução prevista: desativar esses alertas.                              #
# - Identificação de Sistema Operacional Ubuntu, APENAS!                       #
#      Solução prevista: quando eu tiver acesso a outros sistemas operacionais #
#      adaptarei o código para isso. Sugestões são bem vindas para melhorar a  #
#      versatilidade do script.                                                #
#                                                                              #
################################################################################

################################################################################
###                Execução e Gerenciamento das Simulações                   ###
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -###
### Aqui neste script está toda a execução das simulações, tudo previamente  ###
### preparado para lidar com as configurações realizadas no arquivo          ###
### CONFIGURATIONS.py. A princípio, nenhuma modificação é requerida aqui.    ###
### Eu suspeito ter conseguido realizar a generalização adequada. Claro, há  ###
### condições e especificações bem pontuais de experimentos desejados por    ###
### alguns pesquisadores, que fazem com que esse script não funcione como    ###
### desejável. Modificações são bem vindas.                                  ###
################################################################################

############################################
## Importações de bibliotecas necessárias ##
############################################

import json
import os
import subprocess
import platform
from subprocess import PIPE
from time import sleep

# para mostrar os gráficos
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

# Esse é o arquivo de configuração
import CONFIGURATIONS as CFG

#############
## Classes ##
#############

# classe experimento. Aqui eu armazeno todos os dados essenciais
# para possibilitar a criação de cada experimento. Aproveito a
# existência da classe para gerenciar a sua execução


class EXPERIMENT:
    # cada experimento vai receber uma lista
    def __init__(self, idx=0, core=0, cq=0, resolution=CFG.VIDEOS_LIST[0][0], video=CFG.VIDEOS_LIST[0][1], extra_param='', is_there_many_set_of_experiments=False, fps=0):
        # identificador único do experimento
        self.index = idx
        # número do núcleo em que o experimento irá ser executado
        self.core = str(core)
        # valor do CQ do experimento
        self.cq = str(cq)

        # Alan
        extensao = video[-4::]

        # nome do vídeo/pasta do experimento
        self.video_name = video.replace(extensao, '')
        # caminho completo do vídeo
        self.video_file = CFG.VIDEOS_PATH[resolution] + video
        print(self.video_file)
        # identificador se o vídeo já foi enviado para processamento
        self.executed = False
        # identificador se o vídeo já finalizou seu processamento
        self.finished = False
        # identificador se há vários conjuntos de experimentos
        self.many_experiments = is_there_many_set_of_experiments
        # configuração extra que foi incluida
        self.extra_param = extra_param

        # quando finalizar, eu já posso capturar os dados para cálculos de BD-rate
        self.psnr_y = None
        self.bitrate = None
        self.time = None

        # Alan -->
        # Pega infos do vídeo (largura, altura e fps)
        i = j = 0
        fps = largura = altura = ''
        for x in video:
            if (x == '_'):
                i += 1
            if (x == 'x'):
                j += 1
            if (i == 1 and j == 0 and x.isnumeric()):
                largura = str(largura) + str(x)
            elif(i == 1 and j == 1 and x.isnumeric()):
                altura = str(altura) + str(x)
            if (i == 2 and x.isnumeric()):
                fps = str(fps) + str(x)
        #print("fps do vídeo", fps)
        #print("largura do vídeo", largura)
        #print("altura do vídeo", altura)
        # Alan <--

        # linha de comando que será aplicado ao experimento
        # e também é obtido o arquivo de log após o fim do experimento
        self.command, self.outputlog = CFG.GENERATE_COMMAND(self.core,
                                                            self.cq,
                                                            self.video_name,
                                                            self.video_file,
                                                            self.extra_param,
                                                            fps, largura, altura)  # Alan - passei valores para o configurations.py

        # texto de identificação do processo no terminal
        cmd = self.command.split(CFG.CODEC_NAME)[1]
        #cmd = cmd.split(extensao)[0]
        self.terminal_command = cmd
        #print("\n", cmd, "\n")

    # textinho para mostrar valores básicos do experimento
    def printable(self):
        if self.finished:
            txt = "[X]"
        else:
            txt = "[ ]"
        txt += "CORE=" + self.core + "\tCQ=" + self.cq + "\tVIDEO=" + self.video_name

        if self.many_experiments:
            txt += "\tSET='" + self.extra_param + "'"

        if CFG.VERBOSE:
            print(txt)
        printlog(txt)

    # nos backup da vida, preciso reinterpretar os dados json
    def update(self, data):
        self.__dict__.update(data)

    # Função que grava em um csv os dados que recebe
    def export(self):
        filename = self.video_name + '/summary_of_all_data.csv'
        csv = open(filename, 'a')
        if os.path.getsize(filename) == 0:
            csv.write("set, cq, psnr_y, bitrate, time\n")
        csv.write(self.extra_param + "," + self.cq + "," +
                  str(self.psnr_y) + "," + str(self.bitrate) + "," + str(self.time))
        csv.close()


####################################################################

# classe que armazena todos os experimentos que serão executados
class LIST_OF_EXPERIMENTS:
    # inicio a classe com todos os experimentos possíveis
    # SELEÇÃO FIXA DE NÚCLEOS
    def __init__(self):
        iterate_core = 0
        idx = 0
        # lista de experimentos
        self.LIST = []

        # coleciono todas as configurações possíveis
        extra_params = ['']
        extra_params = [*extra_params, *CFG.EXTRA_PARAMS]

        # identifico se há mais de um conjunto de experimentos
        more_than_one_set_of_experiments = len(extra_params) > 1

        # de cada vídeo e cada CQ e cada configuração extra, gero os experimentos
        for resolution, video in CFG.VIDEOS_LIST:
            for cq in CFG.CQ_LIST:
                for extra_p in extra_params:
                    exp = EXPERIMENT(idx,
                                     CFG.ALLOWED_CORES[iterate_core],
                                     cq,
                                     resolution,
                                     video,
                                     extra_p,
                                     more_than_one_set_of_experiments)

                    self.LIST.append(exp)
                    iterate_core += 1
                    idx += 1
                    if iterate_core >= CFG.MAX_CORES:
                        iterate_core = 0
        # controlador de experimentos existentes
        self.MAX_EXPERIMENTS = len(self.LIST)
        # informa quantos experimentos já foram finalizados
        self.TOTAL_FINALIZED = 0

        if(self.load_backup()):
            if CFG.VERBOSE:
                print("Dados do backup foram recuperados com sucesso!")
            printlog("Dados do backup foram recuperados com sucesso!")

    # retorna um experimento de acordo com o seu índice
    def get_experiment_by_idx(self, idx):
        if(idx >= self.MAX_EXPERIMENTS):
            if CFG.VERBOSE:
                print("FALHA F1: tentativa ilegal de acesso à lista de experimentos")
            printlog("FALHA F1: tentativa ilegal de acesso à lista de experimentos")
            return None
        return self.LIST[idx]

    # manda rodar um experimento com base em seu index
    def execute_experiment_by_idx(self, idx):
        if(idx >= self.MAX_EXPERIMENTS):
            if CFG.VERBOSE:
                print("FALHA F2: tentativa ilegal de acesso à lista de experimentos")
            printlog("FALHA F2: tentativa ilegal de acesso à lista de experimentos")
            return None
        exp = self.LIST[idx]

        # caso for a primeira vez que o video vai ser codificado,
        # criar nova pasta
        if(not os.path.exists(exp.video_name)):
            os.system('mkdir ' + exp.video_name)
            for cq in CFG.CQ_LIST:
                os.system('mkdir ' + exp.video_name + '/cq_' + str(cq))
                os.system('mkdir ' + exp.video_name +
                          '/cq_' + str(cq) + '/log')
                os.system('mkdir ' + exp.video_name +
                          '/cq_' + str(cq) + '/webm')

        # executa o comando em modo terminal
        subprocess.call(exp.command, shell=True)

        exp.executed = True

    # quando um experimento finaliza, tirar ele da lista de "em execução"
    # além disso, obtenho os valores dos arquivos e salvo eles em um csv
    # no final, mostro tudo que já foi finalizado
    def finishing_experiment(self, idx):
        if(idx >= self.MAX_EXPERIMENTS):
            if CFG.VERBOSE:
                print("FALHA F3: tentativa ilegal de acesso à lista de experimentos")
            printlog("FALHA F3: tentativa ilegal de acesso à lista de experimentos")
            return None
        exp = self.LIST[idx]
        exp.finished = True
        exp.psnr_y, exp.bitrate, exp.time = CFG.get_psnr_bitrate_time(
            exp.outputlog)
        exp.export()
        self.TOTAL_FINALIZED += 1
        self.save_backup()
        self.print_list_of_experiment_finalized()

    # informa se ainda há experimentos a serem executados
    def are_there_experiments_waiting(self):
        if (self.TOTAL_FINALIZED == self.MAX_EXPERIMENTS):
            return False
        return True

    # retorna o próximo experimento a ser executado para o núcleo informado
    def get_next_free_experiment_on_core(self, core):
        for exp in self.LIST:
            if (exp.finished):
                continue

            if (exp.executed):
                continue

            if(exp.core == str(core)):
                return exp.index

        # Se não há mais nada, então retornar valor "inválido"
        return -1

    # mostra todos os processos em execução no momento
    def print_list_of_experiment_in_execution(self):
        if CFG.VERBOSE:
            print("Simulações que estão sendo executadas:")
        printlog("Simulações que estão sendo executadas:")
        for exp in self.LIST:
            if(exp.executed):
                if(not exp.finished):
                    exp.printable()
        if CFG.VERBOSE:
            print()
        printlog()

    # mostra todos os processos já finalizados
    def print_list_of_experiment_finalized(self):
        if CFG.VERBOSE:
            print("Lista de simulações finalizadas")
        printlog("Lista de simulações finalizadas")
        for exp in self.LIST:
            if(exp.finished):
                exp.printable()
        if CFG.VERBOSE:
            print()
        printlog()

    # mostra todos os processos aguardando execução
    def print_list_of_experiment_waiting(self):
        if CFG.VERBOSE:
            print("Lista de simulações aguardando na fila:")
        printlog("Lista de simulações aguardando na fila:")
        for exp in self.LIST:
            if(not exp.executed):
                exp.printable()
        if CFG.VERBOSE:
            print()
        printlog()

    # mostra todos os processos da lista
    def print_list_of_experiment(self):
        if CFG.VERBOSE:
            print("Lista completa de simulações")
        printlog("Lista completa de simulações")
        for exp in self.LIST:
            exp.printable()
        if CFG.VERBOSE:
            print()
        printlog()

    # função específica para treinos
    # elimina parte dos experimentos para deixar apenas
    # a quantidade informada pelo parâmetro
    def dropTo(self, untilNum):
        self.LIST = self.LIST[:untilNum]
        self.MAX_EXPERIMENTS = len(self.LIST)

    # função que exporta em linha de comando todos os experimentos
    def export_commands(self):
        for exp in self.LIST:
            if CFG.VERBOSE:
                print(exp.command)
            printlog(exp.command)

    # exporta a classe inteira para um arquivo de backup
    def save_backup(self):
        backup_file = open('backup.json', 'w')
        jsoned = json.dumps(self, default=lambda o: o.__dict__)
        backup_file.write(jsoned)
        backup_file.close()
        if CFG.VERBOSE:
            print("Arquivo de backup finalizado")
        printlog("Arquivo de backup finalizado")

    # carrega os dados salvos, caso houver algum arquivo de backup
    # caso sucesso, retornar verdadeiro
    def load_backup(self):
        if(os.path.exists('backup.json')):
            backup_file = open('backup.json', 'r')
            jsoned = json.load(backup_file)
            self.__dict__.update(jsoned)
            list_in_dict = self.LIST
            self.LIST = []
            for dct in list_in_dict:
                exp = EXPERIMENT()
                exp.update(dct)
                if(exp.executed):
                    # Nos casos de vídeos que iniciaram
                    # mas não finalizaram, deve-se
                    # recomeçar eles
                    if(not(exp.finished)):
                        exp.executed = False
                self.LIST.append(exp)
            backup_file.close()
            if CFG.VERBOSE:
                print("Recarregamento dos dados efetuada com sucesso")
            printlog("Recarregamento dos dados efetuada com sucesso")
            if CFG.VERBOSE:
                print("Os experimentos finalizados até o momento:")
            printlog("Os experimentos finalizados até o momento:")
            self.print_list_of_experiment_finalized()
            if CFG.VERBOSE:
                print()
            printlog()
            return True
        return False


####################
## Funções Gerais ##
####################


#  !!!! A seguinte função NÃO É MINHA !!!!
# Código original em https://github.com/shengbinmeng/Bjontegaard_metric/blob/master/bjontegaard_metric.py
# Recebe quatro vetores, e calcula a curva entre eles.
# Quando colocamos o piecewise=1, os valores de BD-rate retornam com maior confiança!
def BD_RATE(R1, PSNR1, R2, PSNR2, piecewise=0):
    lR1 = np.log(R1)
    lR2 = np.log(R2)

    # rate method
    p1 = np.polyfit(PSNR1, lR1, 3)
    p2 = np.polyfit(PSNR2, lR2, 3)

    # integration interval
    min_int = max(min(PSNR1), min(PSNR2))
    max_int = min(max(PSNR1), max(PSNR2))

    # find integral
    if piecewise == 0:
        p_int1 = np.polyint(p1)
        p_int2 = np.polyint(p2)

        int1 = np.polyval(p_int1, max_int) - np.polyval(p_int1, min_int)
        int2 = np.polyval(p_int2, max_int) - np.polyval(p_int2, min_int)
    else:
        lin = np.linspace(min_int, max_int, num=100, retstep=True)
        interval = lin[1]
        samples = lin[0]
        v1 = scipy.interpolate.pchip_interpolate(
            np.sort(PSNR1), lR1[np.argsort(PSNR1)], samples)
        v2 = scipy.interpolate.pchip_interpolate(
            np.sort(PSNR2), lR2[np.argsort(PSNR2)], samples)
        # Calculate the integral using the trapezoid method on the samples.
        int1 = np.trapz(v1, dx=interval)
        int2 = np.trapz(v2, dx=interval)

    # find avg diff
    avg_exp_diff = (int2-int1)/(max_int-min_int)
    avg_diff = (np.exp(avg_exp_diff)-1)*100
    return avg_diff


# Faz uma busca pelos processos em execução e verifica se determinado experimento
# ainda está ou não sendo executado.
# recebe como entrada o parâmetro que foi submetido para execução e o número do core
def exists_command_being_executed_on_core(cmd, core):
    # no terminal eu digitaria:
    # ps -eo psr,cpu,cmd | grep -E  "^[[:space:]]+[[:space:]]+CORE"

    # Aqui eu pego a lista de processos que estão no core X
    regex = "^[[:space:]]+" + str(core)
    p1 = subprocess.Popen(['ps', '-eo', 'psr,cpu,cmd'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-E', r'{}'.format(regex)],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    cmd_comp = cmd.split(' > ')[0]

    # aqui estarão a lista de todos os processos que estão rodando no núcleo pesquisado
    lines = p2.communicate()[0].decode("utf-8")
    # Agora verifico se existe a linha de comando informada entre os processos buscados
    print(lines)
    if(cmd_comp in lines):
        print("SAFE")
        print(cmd_comp)
        return True
    else:
        print("NOT! SAFE")
        print(cmd_comp)
        return False

# A função é bem similar ao de cima, só que eu olho para todos os núcleos
# atrás de alguma função que tenha o nome do codificador que estou utilizando.
# Essa função serve para manter esse script aguardando até o real fim de todas
# as simulações, de forma a possibilitar a geração dos BD-rates.


def is_there_any_codec_in_execution():
    # no terminal eu digitaria:
    # ps -eo psr,cpu,cmd | grep CODEC"

    # Aqui eu pego a lista de processos que estão rodando
    p1 = subprocess.Popen(['ps', '-eo', 'psr,cpu,cmd'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-E', CFG.CODEC_NAME],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    # aqui estarão a lista de todos os processos que estão rodando no núcleo pesquisado
    lines = p2.communicate()[0].decode("utf-8")

    if len(lines) > 0:
        # ainda tem coisa rodando
        return True
    return False


# Função que grava em um csv os dados de BD-rate e tempo calculados
def export_to_csv(video_folder, cfg_set, bdrate, time):
    filename = video_folder + '/summary_of_BD-rate_Time.csv'
    csv = open(filename, 'w')
    if os.path.getsize(filename) == 0:
        csv.write("configuration, bdrate, time cfg / time anchor\n")
    csv.write(cfg_set + "," + str(bdrate) + "," + str(time))
    csv.close()


# Função que lê os dados de psnr e bitrate para gerar um gráfico com a curva bd-rate
# entradas:
#     p_1, psnr âncora (dados do arquivo out.log)
#     b_1, bitrate âncora (dados do arquivo out.log)
#     p_2, psnr experimento (dados do arquivo out_set_EXPERIMENTO.log)
#     p_2, bitrate experimento (dados do arquivo out_set_EXPERIMENTO.log)
def plot_bdrate_curve(p_1, b_1, p_2, b_2, video_folder, experiment_text, bdrate):
    # vou transformar os quatro vetores em dois DataFrames,
    # só pra aproveitar um código que já tenho
    data1 = []
    data2 = []
    for i in range(len(p_1)):
        data1.append([b_1[i], p_1[i]])
        data2.append([b_2[i], p_2[i]])

    anchor = pd.DataFrame(data1, columns=['bitrate', 'psnr_y'])
    versus = pd.DataFrame(data2, columns=['bitrate', 'psnr_y'])

    # Preparo os dados para mostrar no gráfico

    # tamanho do grafico
    sns.set(rc={'figure.figsize': (15, 10)})
    # tamanho da fonte
    sns.set(font_scale=2)

    # Mando plotar as linhas
    ax = sns.lineplot(data=anchor,
                      x='bitrate',
                      y='psnr_y',
                      linewidth=2.5,
                      marker='o',
                      markersize=14)
    ax = sns.lineplot(data=versus,
                      x='bitrate',
                      y='psnr_y',
                      linewidth=2.5,
                      marker='s',
                      markersize=14,
                      ax=ax)

    # digo o texto dos eixos
    ax.set(xlabel="bitrate (bps)",
           ylabel="PSNR-Y (dB)")

    # adiciono a legenda da imagem
    ax.legend(labels=['anchor configuration',
                      experiment_text + ' configuration'],
              loc='lower right')

    # adicionando o valor do BD-rate no gráfico
    # CASO não quiser, só comentar a linha de baixo
    # posição: x = o menor bitrate; y = maior psnr
    ax.text(b_1[-1],
            p_1[0],
            "BD-rate {:.3f}%".format(bdrate),
            fontsize=20,
            verticalalignment='top')

    # mando mostrar a grade
    plt.grid(True)

    # salvando o gráfico
    plt.savefig(video_folder + '/bdrate_curve_' + experiment_text + '.png')

    # fechando o gráfico
    plt.clf()

# Solução que achei para que as saídas do script fiquem salvas em um arquivo de log


def printlog(text="", end="\n"):
    f = open("script_log.log", 'a')
    f.write(text + end)
    f.close()


################
## __MAIN__() ##
################


#########################################################
##                   baixa o libaom                    ##
## Se for utilizar OUTRO codificador que não o libaom, ##
## então modificar o código para baixe corretamente.   ##
#########################################################

if CFG.DOWNLOAD:
    CFG.DO_DOWNLOAD()


#############################################################
##                    Compila o libaom                     ##
## Se precisar adicionar algo extra ou for utilizar OUTRO  ##
## codificador que não o libaom, então modificar o código. ##
#############################################################

if CFG.COMPILE:
    # captura a versão do sistema operacional e envia.
    # Isso é importante pois pode haver condições diferentes
    # de compilação do programa a depender so sistema operacional
    CFG.DO_COMPILE(float(platform.dist()[1]))


###############################################################
##                     Executa um Teste                      ##
## O código abaixo gera todas as simulações e manda executar ##
## somente a primeira simulação dentre todas.                ##
###############################################################

if CFG.TESTE:
    # crio a lista de experimentos
    list_of_experiments = LIST_OF_EXPERIMENTS()

    # mostro quantas simulações são possíveis de serem realizadas
    if CFG.VERBOSE:
        print("Com a configuração estabelecida, há um total de ",
              list_of_experiments.MAX_EXPERIMENTS,
              " simulações que podem ser realizadas.")
    printlog("Com a configuração estabelecida, há um total de ",
             list_of_experiments.MAX_EXPERIMENTS,
             " simulações que podem ser realizadas.")

    if CFG.VERBOSE:
        print("Iniciando a simulação 1")
    printlog("Iniciando a simulação 1")
    # Dado o primeiro core, pego o experimento livre alocado para ele
    idx = list_of_experiments.get_next_free_experiment_on_core(
        CFG.ALLOWED_CORES[0])
    # capturo o experimento em uma variável, fica mais fácil de controlar
    exp = list_of_experiments.get_experiment_by_idx(idx)
    # Mostro qual é o experimento que vai ser executado
    exp.printable()
    # mando executar o experimento
    list_of_experiments.execute_experiment_by_idx(idx)
    while (is_there_any_codec_in_execution()):
        if CFG.VERBOSE:
            print("\nEsperando Simulações em Andamento\n")
        printlog("\nEsperando Simulações em Andamento\n")
        sleep(CFG.WAITING_TIME)
    # quando ele terminar, finalizo ele
    list_of_experiments.finishing_experiment(idx)
    if CFG.VERBOSE:
        print("Simulação 1 finalizada.")
    printlog("Simulação 1 finalizada.")
    # Mostrando na mão os dados do arquivo de saída
    exp = list_of_experiments.get_experiment_by_idx(idx)
    if CFG.VERBOSE:
        print("A simulação apresentou os seguintes dados:")
        print("PSNR-Y:", str(exp.psnr_y), "dB")
        print("bitrate:", str(exp.bitrate), "bps")
        print("tempo de execução:", str(exp.time), "ms")

    printlog("A simulação apresentou os seguintes dados:")
    printlog("PSNR-Y:", str(exp.psnr_y), "dB")
    printlog("bitrate:", str(exp.bitrate), "bps")
    printlog("tempo de execução:", str(exp.time), "ms")

####################################################################
##                 Executa Todas as Simulações                    ##
## Aqui há a geração das simulações e gerenciamento das execuções ##
####################################################################

if CFG.EXECUTE:
    # crio a lista de experimentos em si
    list_of_experiments = LIST_OF_EXPERIMENTS()

    ################
    # Em casos de testes locais, reduzo o número de experimentos
    # list_of_experiments.dropTo(CFG.MAX_CORES)
    ################

    if(list_of_experiments.MAX_EXPERIMENTS <= CFG.MAX_CORES):
        # neste caso, posso rodar todos sem nenhum problema
        for core in CFG.ALLOWED_CORES:
            idx = list_of_experiments.get_next_free_experiment_on_core(core)
            list_of_experiments.get_experiment_by_idx(idx).printable()
            list_of_experiments.execute_experiment_by_idx(idx)
    else:
        # crio a lista de índices de experimentos com dados vazios
        list_index = [None] * CFG.MAX_CORES

        # enquanto houver experimentos pra executar, repita
        while(list_of_experiments.are_there_experiments_waiting()):
            # vai dar uma passada em todos os indices da lista
            for idxList in range(CFG.MAX_CORES):
                # caso o idx estiver nulo, significa que não foi inicializado
                if(list_index[idxList] == None):
                    # busco o experimento
                    list_index[idxList] = list_of_experiments.get_next_free_experiment_on_core(
                        CFG.ALLOWED_CORES[idxList])
                    # e já mando executar ele
                    list_of_experiments.get_experiment_by_idx(
                        list_index[idxList]).printable()
                    list_of_experiments.execute_experiment_by_idx(
                        list_index[idxList])

                # caso o idx estiver negativo, é pq não tem mais experimentos para aquele núcleo
                if(list_index[idxList] < 0):
                    continue

                # verifico se o experimento ainda está rodando
                if(exists_command_being_executed_on_core(
                        list_of_experiments.get_experiment_by_idx(
                            list_index[idxList]).terminal_command,
                        CFG.ALLOWED_CORES[idxList])):
                    if CFG.VERBOSE:
                        print(
                            "Núcleo " + str(CFG.ALLOWED_CORES[idxList]) + " ocupado, aguarde...")
                    printlog(
                        "Núcleo " + str(CFG.ALLOWED_CORES[idxList]) + " ocupado, aguarde...")
                    continue
                else:
                    if CFG.VERBOSE:
                        print(
                            "Núcleo " + str(CFG.ALLOWED_CORES[idxList]) + " liberado, aguarde...")
                    printlog(
                        "Núcleo " + str(CFG.ALLOWED_CORES[idxList]) + " liberado, aguarde...")
                    # já terminou, então preciso finalizar o experimento
                    list_of_experiments.finishing_experiment(
                        list_index[idxList])
                    # procuro um novo experimento para rodar
                    list_index[idxList] = list_of_experiments.get_next_free_experiment_on_core(
                        CFG.ALLOWED_CORES[idxList])
                    # Caso o valor for negativo, já acabaram os experimentos para aquele núcleo
                    if(list_index[idxList] < 0):
                        if CFG.VERBOSE:
                            print("Experimentos do núcleo " +
                                  str(CFG.ALLOWED_CORES[idxList]) + " já finalizaram")
                        printlog("Experimentos do núcleo " +
                                 str(CFG.ALLOWED_CORES[idxList]) + " já finalizaram")
                        continue
                    else:
                        # mando executar
                        list_of_experiments.get_experiment_by_idx(
                            list_index[idxList]).printable()
                        list_of_experiments.execute_experiment_by_idx(
                            list_index[idxList])

            if CFG.VERBOSE:
                print("\nEsperando Simulações em Andamento\n")
            printlog("\nEsperando Simulações em Andamento\n")
            sleep(CFG.WAITING_TIME)

    # todas as simulações estão rodando, mas...
    # é preciso esperar que eles de fato terminem!
    while (is_there_any_codec_in_execution()):
        if CFG.VERBOSE:
            print("\nEsperando Simulações em Andamento\n")
        printlog("\nEsperando Simulações em Andamento\n")
        sleep(CFG.WAITING_TIME)

    if CFG.VERBOSE:
        print("\n\nFim das Simulações\n")
    printlog("\n\nFim das Simulações\n")

    # Agora posso pegar todos os dados e fazer os BD-rates, se houver:
    # 1) ao menos UM parâmetro extra, pois preciso comparar duas configurações
    # 2) ao menos QUATRO CQs, pois a curva de BD-rate requer isso!
    if ((len(CFG.EXTRA_PARAMS) > 0) and (len(CFG.CQ_LIST) > 3)):
        if CFG.VERBOSE:
            print("Ativando sistema de geração automática de BD-rate")
        printlog("Ativando sistema de geração automática de BD-rate")

        # lista de todos os conjuntos de simulação
        extra_params = ['']
        extra_params = [*extra_params, *CFG.EXTRA_PARAMS]

        # Ainda é preciso otimizar esses loops. Ainda está muito força-bruta

        # vou utilizar uma matriz tridimensional para capturar os valores dos experimentos
        # a ideia geral: matrix[video][extra_param][cq].append([psnr, bitrate, time])
        M3D = [None] * len(CFG.VIDEOS_LIST)
        video_keys = []
        for i in range(len(CFG.VIDEOS_LIST)):
            # A lista de vídeos é um array duplo, só me interessa um dos valores
            video_keys.append(CFG.VIDEOS_LIST[i][1])
            M3D[i] = [None] * len(extra_params)
            for j in range(len(extra_params)):
                M3D[i][j] = [None] * len(CFG.CQ_LIST)

        if CFG.VERBOSE:
            print("Capturando valores dos arquivos...", end="\t")
        printlog("Capturando valores dos arquivos...", end="\t")
        # para cada simulação...
        for idx in range(0, list_of_experiments.MAX_EXPERIMENTS):
            exp = list_of_experiments.get_experiment_by_idx(idx)

            idxVideo = video_keys.index(exp.video_name)
            idxParam = extra_params.index(exp.extra_param)
            idxCQ = CFG.CQ_LIST.index(int(exp.cq))

            M3D[idxVideo][idxParam][idxCQ] = [
                exp.psnr_y, exp.bitrate, exp.time]

        if CFG.VERBOSE:
            print("Finalizado!")
            print("Gerando percentuais...", end="\t")
        printlog("Finalizado!")
        printlog("Gerando percentuais...", end="\t")

        #bdrate = BD_RATE([])
        BDRATE = []

        # de cada vídeo...
        for vid in video_keys:
            idxVideo = video_keys.index(vid)

            # pego os valores da configuração âncora
            anchor_psnr = []
            anchor_bitrate = []
            anchor_time = []

            # Capturo os valores âncoras
            for cq in range(len(CFG.CQ_LIST)):
                # de cada vídeo, pego o primeiro parâmetro e todos os CQs
                out = M3D[idxVideo][0][cq]
                anchor_psnr.append(out[0])
                anchor_bitrate.append(out[1])
                anchor_time.append(out[2])

            # Para cada parâmetro extra, capturo os valores e processo:
            # a. O percentual de BD-rate
            # b. o gráfico da curva de BD-rate
            # c. O percentual de tempo de execução
            for param in range(1, len(extra_params)):
                versus_psnr = []
                versus_bitrate = []
                versus_time = []
                for cq in range(len(CFG.CQ_LIST)):
                    # de cada vídeo, pego o primeiro parâmetro e todos os CQs
                    tmp = M3D[idxVideo][param][cq]
                    versus_psnr.append(tmp[0])
                    versus_bitrate.append(tmp[1])
                    versus_time.append(tmp[2])

                bdrate = BD_RATE(anchor_bitrate,
                                 anchor_psnr,
                                 versus_bitrate,
                                 versus_psnr,
                                 1)
                timecomparison = sum(versus_time) / sum(anchor_time)

                plot_bdrate_curve(anchor_psnr,
                                  anchor_bitrate,
                                  versus_psnr,
                                  versus_bitrate,
                                  vid,
                                  extra_params[param],
                                  bdrate)

                export_to_csv(vid,
                              extra_params[param],
                              bdrate,
                              timecomparison)

        if CFG.VERBOSE:
            print("Finalizado!")
        printlog("Finalizado!")

    print("Script Gerenciador finalizado com sucesso!")
    printlog("Script Gerenciador finalizado com sucesso!")

print("\n\nscript desevolvido por amborges@inf.ufpel.edu.br\n")
printlog("\n\nscript desevolvido por amborges@inf.ufpel.edu.br\n")
