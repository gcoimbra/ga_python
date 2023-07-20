import math
import random
import time
import statistics

# Problema da Treliça

l = 100
P = 2
sigma = 2

def funcaoTrelica(x1, x2):
    return ((2*math.sqrt(2)*x1 + x2) * l)

def validaXTrelica(x):
    if(x >= 0 and x <= 1):
        return True
    return False

def restricaoG1Trelica(x1, x2, P, sigma):
    if((((((math.sqrt(2)*x1) + x2)/((math.sqrt(2)*(x1**2)) + 2*x1*x2)) * P) - sigma) <= 0):
        return True
    return False

def restricaoG2Trelica(x1, x2, P, sigma):
    if(((((x2)/((math.sqrt(2)*(x1**2)) + 2*x1*x2)) * P) - sigma) <= 0):
        return True
    return False

def restricaoG3Trelica(x1, x2, P, sigma):
    if((((1)/((math.sqrt(2)*x2) + x1) * P) - sigma) <= 0):
        return True
    return False

def validaTresRestricoesTrelica(x1, x2, intervaloMin, intervaloMax):

    if(not ((x1 >= intervaloMin and x1 <= intervaloMax) and (x2 >= intervaloMin and x2 <= intervaloMax))):
        return False
    if(not restricaoG1Trelica(x1, x2, P, sigma)):
        return False
    if(not restricaoG2Trelica(x1, x2, P, sigma)):
        return False
    if(not restricaoG3Trelica(x1, x2, P, sigma)):
        return False
    
    return True

def geraSolucaoAleatoriaTrelica(intervaloMin, intervaloMax):
    
    while(True):
        
        x1 = random.uniform(intervaloMin, intervaloMax)
        x2 = random.uniform(intervaloMin, intervaloMax)
        
        if(validaTresRestricoesTrelica(x1, x2, intervaloMin, intervaloMax)):
            break

    return [x1, x2]

# Problema do Vaso de Pressão

multiploVasoPressao = 0.0625

def eefuncaoVasoPressao(x1, x2, x3, x4):
    return ((0.6224*(x1*multiploVasoPressao)*x3*x4) + (1.7781*(x2*multiploVasoPressao)*(x3**2)) + (3.1661*((x1*multiploVasoPressao)**2)*x4) + (19.84*((x1*multiploVasoPressao)**2)*x3))

def restricaoG1VasoPressao(x1, x3):
    if((-(x1*multiploVasoPressao) + 0.0193*x3) <= 0):
        return True
    return False

def restricaoG2VasoPressao(x2, x3):
    if((-(x2*multiploVasoPressao) + 0.00954*x3) <= 0):
        return True
    return False

def restricaoG3VasoPressao(x3, x4):
    if(((-math.pi*(x3**2)*x4) - ((4/3)*math.pi*(x3**3)) + 1296000) <= 0):
        return True
    return False

def restrucaiG4VasoPressao(x4):
    if((x4 - 240) <= 0):
        return True
    return False

def validaQuatroRestricoesVasoPressao(x1, x2, x3, x4, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max):

    if(not (((x1*multiploVasoPressao) >= intervaloX1X2Min) and ((x1*multiploVasoPressao) <= intervaloX1X2Max))):
        return False
    if(not (((x2*multiploVasoPressao) >= intervaloX1X2Min) and ((x2*multiploVasoPressao) <= intervaloX1X2Max))):
        return False
    if(not ((x3 >= intervaloX3X4Min) and (x3 <= intervaloX3X4Max))):
        return False
    if(not ((x4 >= intervaloX3X4Min) and (x4 <= intervaloX3X4Max))):
        return False

    if(not restricaoG1VasoPressao(x1, x3)):
        return False
    if(not restricaoG2VasoPressao(x2, x3)):
        return False
    if(not restricaoG3VasoPressao(x3, x4)):
        return False
    if(not restrucaiG4VasoPressao(x4)):
        return False

    return True

def geraSolucaoAleatoriaVasoPressao(intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max):

    while(True):

        x1 = int(round(random.uniform((intervaloX1X2Min/multiploVasoPressao), (intervaloX1X2Max/multiploVasoPressao)), 0))
        x2 = int(round(random.uniform((intervaloX1X2Min/multiploVasoPressao), (intervaloX1X2Max/multiploVasoPressao)), 0))
        x3 = random.uniform(intervaloX3X4Min, intervaloX3X4Max)
        x4 = random.uniform(intervaloX3X4Min, intervaloX3X4Max)
        
        if(validaQuatroRestricoesVasoPressao(x1, x2, x3, x4, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max)):
            break

    return [x1, x2, x3, x4]

# Algoritmo Genético

def selecaoPorTorneioTrelica(populacao, tamanhoAmostra, qtdTorneios):
    
    tamanhoPopulacao = len(populacao)
    
    listaVencedoresTorneios = []

    for i in range(qtdTorneios):

        indicesAmostraPopulacao = random.sample(range(tamanhoPopulacao), tamanhoAmostra)
        
        indiceMelhorSolucao = indicesAmostraPopulacao[0]
        x1, x2 = populacao[indiceMelhorSolucao]

        for indice in indicesAmostraPopulacao[1:]:
            x1Concorrente, x2Concorrente = populacao[indice]
            if(funcaoTrelica(x1Concorrente, x2Concorrente) < funcaoTrelica(x1, x2)):
                x1 = x1Concorrente
                x2 = x2Concorrente
                indiceMelhorSolucao = indice
        
        listaVencedoresTorneios.append(indiceMelhorSolucao)
    
    return list(dict.fromkeys(listaVencedoresTorneios))

def selecaoPorTorneioVasoPressao(populacao, tamanhoAmostra, qtdTorneios):
    
    tamanhoPopulacao = len(populacao)

    listaVencedoresTorneios = []

    for i in range(qtdTorneios):

        indicesAmostraPopulacao = random.sample(range(tamanhoPopulacao), tamanhoAmostra)
        
        indiceMelhorSolucao = indicesAmostraPopulacao[0]
        x1, x2, x3, x4 = populacao[indiceMelhorSolucao]

        for indice in indicesAmostraPopulacao[1:]:
            x1Concorrente, x2Concorrente, x3Concorrente, x4Concorrente = populacao[indice]
            if(funcaoVasoPressao(x1Concorrente, x2Concorrente, x3Concorrente, x4Concorrente) < funcaoVasoPressao(x1, x2, x3, x4)):
                x1 = x1Concorrente
                x2 = x2Concorrente
                x3 = x3Concorrente
                x4 = x4Concorrente
                indiceMelhorSolucao = indice
        
        listaVencedoresTorneios.append(indiceMelhorSolucao)
    
    return list(dict.fromkeys(listaVencedoresTorneios))

def randomCruzamentoFlat(valorPai1, valorPai2):
    if(valorPai2 > valorPai1):
        return random.uniform(valorPai1, valorPai2)
    else:
        return random.uniform(valorPai2, valorPai1)

def cruzamentoFlat(pai1, pai2):

    filho = []

    for i in range(len(pai1)):
        filho.append(randomCruzamentoFlat(pai1[i], pai2[i]))
    
    return filho

def cruzamentoDiscreto(pai1, pai2):

    filho1 = []
    filho2 = []

    for i in range(len(pai1)):
        numero = random.sample(range(2), 1)[0]
        if(numero == 0):
            filho1.append(pai1[i])
            filho2.append(pai2[i])
        else:
            filho1.append(pai2[i])
            filho2.append(pai1[i])
    
    return filho1, filho2

def mutacaoPolinomial(filho, intervaloMin, intervaloMax):
    
    sigmaMutacao = random.random()
    nM = 20

    for i in range(len(filho)):
        
        Uk = random.random()

        if(Uk <= 0.5):
            sigmaK = math.pow((2*Uk), (1/(nM+1))) - 1
        else:
            sigmaK = 1 - math.pow((2*(1-Uk)), (1/(nM+1)))
        
        filho[i] += sigmaMutacao*(intervaloMax - intervaloMin)*sigmaK

def mutacaoPolinomialVasoPressao(filho, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max):
    
    sigmaMutacao = random.random()
    nM = 20

    for i in range(len(filho)):
        
        Uk = random.random()

        if(Uk <= 0.5):
            sigmaK = math.pow((2*Uk), (1/(nM+1))) - 1
        else:
            sigmaK = 1 - math.pow((2*(1-Uk)), (1/(nM+1)))
        
        if(i < 2):
            filho[i] += int(round(sigmaMutacao*((intervaloX1X2Max/multiploVasoPressao) - (intervaloX1X2Min/multiploVasoPressao))*sigmaK, 0))
        else:
            filho[i] += sigmaMutacao*(intervaloX3X4Max - intervaloX3X4Min)*sigmaK

def retornaMelhorIndividuoGeracaoTrelica(populacao):

    melhorIndividuo = sorted(populacao, key=lambda item: funcaoTrelica(item[0], item[1]))[0]

    return melhorIndividuo

def retornaMelhorIndividuoGeracaoVasoPressao(populacao):

    melhorIndividuo = sorted(populacao, key=lambda item: funcaoVasoPressao(item[0], item[1], item[2], item[3]))[0]

    return melhorIndividuo
