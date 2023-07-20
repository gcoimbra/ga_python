from funcoes_auxiliares import *

def problemaVasoPressao(qtdGeracoesMaxima, tamanhoPopulacaoInicial):

    print("----- Problema do Vaso de Pressão -----\n")

    agrupamentoGeracoes = {}
    melhoresSolucoesGeracoes = {}

    intervaloX1X2Min = 0; intervaloX1X2Max = 100
    intervaloX3X4Min = 10; intervaloX3X4Max = 200

    print("Configurações do processo evolutivo")
    print("  -> Quantidade de gerações máxima: %d" % qtdGeracoesMaxima)
    print("  -> Tamanho da população inicial: %d" % tamanhoPopulacaoInicial)
    print("  -> Intervalo de X1 e X2: [%.2f, %.2f]" % (intervaloX1X2Min, intervaloX1X2Max))
    print("  -> Intervalo de X3 e X4: [%.2f, %.2f]\n" % (intervaloX3X4Min, intervaloX3X4Max))

    tempoInicial = time.time()

    populacaoInicial = []

    for i in range(tamanhoPopulacaoInicial):
        populacaoInicial.append(geraSolucaoAleatoriaVasoPressao(intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max))

    agrupamentoGeracoes.update({'geracao1': populacaoInicial})

    melhorIndividuoG1 = retornaMelhorIndividuoGeracaoVasoPressao(populacaoInicial)
    melhoresSolucoesGeracoes.update({'geracao1': [melhorIndividuoG1, funcaoVasoPressao(melhorIndividuoG1[0], melhorIndividuoG1[1], melhorIndividuoG1[2], melhorIndividuoG1[3])]})

    print("Geração inicial = %d, tamanho da população = %d" % (1, len(agrupamentoGeracoes['geracao%d' % 1])))

    melhorSolucao = melhoresSolucoesGeracoes['geracao1'][1]
    individuoMelhorSolucao = melhoresSolucoesGeracoes['geracao1'][0]
    geracaoMelhorSolucao = 1
    tentativasSemGanho = qtdGeracoesMaxima * 0.2

    for i in range(2, qtdGeracoesMaxima+1):

        geracaoPai = agrupamentoGeracoes['geracao%d' % (i-1)]
        tamanhoGeracaoPai = len(geracaoPai)

        # Seleção por torneio dos melhores candidatos à procriar

        melhoresCandidatos = -1

        if(tamanhoGeracaoPai == 2):
            melhoresCandidatos = selecaoPorTorneioVasoPressao(geracaoPai, 2, tamanhoPopulacaoInicial)
        elif(tamanhoGeracaoPai >= 3):
            melhoresCandidatos = selecaoPorTorneioVasoPressao(geracaoPai, 3, tamanhoPopulacaoInicial)
        
        if(melhoresCandidatos == -1):
            break
        
        individuosSelecionados = [geracaoPai[indiceMelhor] for indiceMelhor in melhoresCandidatos]

        novaGeracao = []

        for j in range(len(individuosSelecionados)-1):

            # filho1 = cruzamentoFlat(individuosSelecionados[j], individuosSelecionados[j+1])
            # filho2 = cruzamentoFlat(individuosSelecionados[j], individuosSelecionados[j+1])
            
            # Cruzamento discreto - pega aleatoriamente um gene de um dos dois pais (item do vetor) para criar um novo filho.

            filho1, filho2 = cruzamentoDiscreto(individuosSelecionados[j], individuosSelecionados[j+1])

            # Mutação polinomial - modifica os novos filhos para diversificar a nova geração criada.
            # OBS.: só aceita os indivíduos mutados que estão dentro do intervalo válido de solução (Penalização por morte).

            mutacaoPolinomialVasoPressao(filho1, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max)
            if(validaQuatroRestricoesVasoPressao(filho1[0], filho1[1], filho1[2], filho1[3], intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max)):
                novaGeracao.append(filho1)
            
            mutacaoPolinomialVasoPressao(filho2, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max)
            if(validaQuatroRestricoesVasoPressao(filho2[0], filho2[1], filho2[2], filho2[3], intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max)):
                novaGeracao.append(filho2)
        
        if(not novaGeracao):
            break
        
        agrupamentoGeracoes.update({'geracao%d' % (i): novaGeracao})

        melhorIndividuoGeracaoAvaliada = retornaMelhorIndividuoGeracaoVasoPressao(novaGeracao)
        solucaoMelhorIndividuoGeracaoAvaliada = funcaoVasoPressao(melhorIndividuoGeracaoAvaliada[0], melhorIndividuoGeracaoAvaliada[1], melhorIndividuoGeracaoAvaliada[2], melhorIndividuoGeracaoAvaliada[3])
        melhoresSolucoesGeracoes.update({'geracao%d' % (i): [melhorIndividuoGeracaoAvaliada, solucaoMelhorIndividuoGeracaoAvaliada]})

        # Verificando se após criar 20% do máximo de gerações permitidas não houve melhoria.
        if(solucaoMelhorIndividuoGeracaoAvaliada < melhorSolucao):
            melhorSolucao = solucaoMelhorIndividuoGeracaoAvaliada
            individuoMelhorSolucao = melhorIndividuoGeracaoAvaliada
            geracaoMelhorSolucao = i
            tentativasSemGanho = qtdGeracoesMaxima * 0.2
        else:
            if(tentativasSemGanho > 0):
                tentativasSemGanho -= 1
            else:
                break

    idUltimaGeracaoComPopulacao = len(agrupamentoGeracoes) + 1
    tamanhoUltimaGeracaoComPopulacao = 0

    while(tamanhoUltimaGeracaoComPopulacao == 0):
        idUltimaGeracaoComPopulacao -= 1
        tamanhoUltimaGeracaoComPopulacao = len(agrupamentoGeracoes['geracao%d' % (idUltimaGeracaoComPopulacao)])

    print("\nGeração final = %d, tamanho da população = %d\n" % (idUltimaGeracaoComPopulacao, tamanhoUltimaGeracaoComPopulacao))

    agrupamentoGeracoes['geracao1'].sort(key=lambda item: funcaoVasoPressao(item[0], item[1], item[2], item[3]))
    agrupamentoGeracoes['geracao%d' % (idUltimaGeracaoComPopulacao)].sort(key=lambda item: funcaoVasoPressao(item[0], item[1], item[2], item[3]))

    melhorSolucaoG1 = agrupamentoGeracoes['geracao1'][0]
    print("-> Melhor solução para a primeira geração:")
    print("    Geração = %d" % 1)
    print("    X1 = (%d * %f) = %f, X2 = (%d * %f) = %f, X3 = %f e X4 = %f" % (melhorSolucaoG1[0], multiploVasoPressao, melhorSolucaoG1[0]*multiploVasoPressao, melhorSolucaoG1[1], multiploVasoPressao, melhorSolucaoG1[1]*multiploVasoPressao, melhorSolucaoG1[2], melhorSolucaoG1[3]))
    print("    f(x) = %.4f" % funcaoVasoPressao(melhorSolucaoG1[0], melhorSolucaoG1[1], melhorSolucaoG1[2], melhorSolucaoG1[3]))

    melhorSolucaoUltimaG = agrupamentoGeracoes['geracao%d' % (idUltimaGeracaoComPopulacao)][0]
    print("\n-> Melhor solução para a última geração:")
    print("    Geração = %d" % idUltimaGeracaoComPopulacao)
    print("    X1 = (%d * %f) = %f, X2 = (%d * %f) = %f, X3 = %f e X4 = %f" % (melhorSolucaoUltimaG[0], multiploVasoPressao, melhorSolucaoUltimaG[0]*multiploVasoPressao, melhorSolucaoUltimaG[1], multiploVasoPressao, melhorSolucaoUltimaG[1]*multiploVasoPressao, melhorSolucaoUltimaG[2], melhorSolucaoUltimaG[3]))
    print("    f(x) = %.4f" % funcaoVasoPressao(melhorSolucaoUltimaG[0], melhorSolucaoUltimaG[1], melhorSolucaoUltimaG[2], melhorSolucaoUltimaG[3]))

    print("\n-> Melhor solução geral considerando todas as gerações:")
    print("    Geração = %d" % geracaoMelhorSolucao)
    print("    X1 = (%d * %f) = %f, X2 = (%d * %f) = %f, X3 = %f e X4 = %f" % (individuoMelhorSolucao[0], multiploVasoPressao, individuoMelhorSolucao[0]*multiploVasoPressao, individuoMelhorSolucao[1], multiploVasoPressao, individuoMelhorSolucao[1]*multiploVasoPressao, individuoMelhorSolucao[2], individuoMelhorSolucao[3]))
    print("    f(x) = %.4f\n" % melhorSolucao)

    tempoFinal = time.time() - tempoInicial
    print("Tempo de execução: %.2f segundos" % tempoFinal)

    listaSolucoes = [melhoresSolucoesGeracoes[i][1] for i in melhoresSolucoesGeracoes]

    print("\n-> Estatísticas:")
    print("    Média = %.4f" % statistics.mean(listaSolucoes))
    print("    Desvio Padrão = %.4f" % statistics.stdev(listaSolucoes))
    print("    Mínimo = %.4f" % min(listaSolucoes))
    print("    Máximo = %.4f" % max(listaSolucoes))

    return individuoMelhorSolucao, melhorSolucao, tempoFinal

def gerarAnaliseNExecucoesVasoPressao(N, qtdGeracoesMaxima, tamanhoPopulacaoInicial):

    listaIndividuos = []
    listaMelhoresSolucoes = []
    listaTemposExecucao = []
    
    for i in range(N):
        
        print("\n------------ ITERAÇÃO: %d ------------\n" % (i+1))

        individuoMelhorSolucao, melhorSolucao, tempoExecucao = problemaVasoPressao(qtdGeracoesMaxima, tamanhoPopulacaoInicial)

        listaIndividuos.append(individuoMelhorSolucao)
        listaMelhoresSolucoes.append(melhorSolucao)
        listaTemposExecucao.append(tempoExecucao)
    
    melhorIndice = listaMelhoresSolucoes.index(sorted(listaMelhoresSolucoes)[0])
    piorIndice = listaMelhoresSolucoes.index(sorted(listaMelhoresSolucoes)[-1])

    print("\n------------------------ RESULTADOS ------------------------\n\n")
    print("----- Problema do Vaso de Pressão -----\n")
    print("Quantidade de iterações realizadas: %d" % N)
    print("Quantidade de gerações máxima: %d" % qtdGeracoesMaxima)
    print("Tamanho de população máximo: %d" % tamanhoPopulacaoInicial)
    print("Média das soluções: %f, Desvio Padrão das soluções: %f" % (statistics.mean(listaMelhoresSolucoes), statistics.stdev(listaMelhoresSolucoes)))
    print("Menor solução:")
    print("  X1 = %d * (%f) = %f" % (listaIndividuos[melhorIndice][0], multiploVasoPressao, multiploVasoPressao*listaIndividuos[melhorIndice][0]))
    print("  X2 = %d * (%f) = %f" % (listaIndividuos[melhorIndice][1], multiploVasoPressao, multiploVasoPressao*listaIndividuos[melhorIndice][1]))
    print("  X3 = %f" % (listaIndividuos[melhorIndice][2]))
    print("  X4 = %f" % (listaIndividuos[melhorIndice][3]))
    print("  f(x) = %f" % listaMelhoresSolucoes[melhorIndice])
    print("Maior solução:")
    print("  X1 = %d * (%f) = %f" % (listaIndividuos[piorIndice][0], multiploVasoPressao, multiploVasoPressao*listaIndividuos[piorIndice][0]))
    print("  X2 = %d * (%f) = %f" % (listaIndividuos[piorIndice][1], multiploVasoPressao, multiploVasoPressao*listaIndividuos[piorIndice][1]))
    print("  X3 = %f" % (listaIndividuos[piorIndice][2]))
    print("  X4 = %f" % (listaIndividuos[piorIndice][3]))
    print("  f(x) = %f" % listaMelhoresSolucoes[piorIndice])
    print("Média de tempo: %fs, Desvio padrão de tempo: %fs\n" % (statistics.mean(listaTemposExecucao), statistics.stdev(listaTemposExecucao)))
    print("------------------------------------------------------------\n")

gerarAnaliseNExecucoesVasoPressao(N=50, qtdGeracoesMaxima=1000, tamanhoPopulacaoInicial=1000)