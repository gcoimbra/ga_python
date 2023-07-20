from funcoes_auxiliares import *

def problemaTrelica(qtdGeracoesMaxima, tamanhoPopulacaoInicial):

    print("----- Problema da Treliça -----\n")

    agrupamentoGeracoes = {}
    melhoresSolucoesGeracoes = {}

    intervaloMin = 0; intervaloMax = 1

    print("Configurações do processo evolutivo")
    print("  -> Quantidade de gerações máxima: %d" % qtdGeracoesMaxima)
    print("  -> Tamanho da população inicial: %d" % tamanhoPopulacaoInicial)
    print("  -> Intervalo de X1 e X2: [%.2f, %.2f]\n" % (intervaloMin, intervaloMax))

    tempoInicial = time.time()

    populacaoInicial = []

    for i in range(tamanhoPopulacaoInicial):
        populacaoInicial.append(geraSolucaoAleatoriaTrelica(intervaloMin, intervaloMax))

    agrupamentoGeracoes.update({'geracao1': populacaoInicial})

    melhorIndividuoG1 = retornaMelhorIndividuoGeracaoTrelica(populacaoInicial)
    melhoresSolucoesGeracoes.update({'geracao1': [melhorIndividuoG1, funcaoTrelica(melhorIndividuoG1[0], melhorIndividuoG1[1])]})

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
            melhoresCandidatos = selecaoPorTorneioTrelica(geracaoPai, 2, tamanhoPopulacaoInicial)
        elif(tamanhoGeracaoPai >= 3):
            melhoresCandidatos = selecaoPorTorneioTrelica(geracaoPai, 3, tamanhoPopulacaoInicial)
        
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

            mutacaoPolinomial(filho1, intervaloMin, intervaloMax)
            if(validaTresRestricoesTrelica(filho1[0], filho1[1], intervaloMin, intervaloMax)):
                novaGeracao.append(filho1)
            
            mutacaoPolinomial(filho2, intervaloMin, intervaloMax)
            if(validaTresRestricoesTrelica(filho2[0], filho2[1], intervaloMin, intervaloMax)):
                novaGeracao.append(filho2)
        
        if(not novaGeracao):
            break
        
        agrupamentoGeracoes.update({'geracao%d' % (i): novaGeracao})

        melhorIndividuoGeracaoAvaliada = retornaMelhorIndividuoGeracaoTrelica(novaGeracao)
        solucaoMelhorIndividuoGeracaoAvaliada = funcaoTrelica(melhorIndividuoGeracaoAvaliada[0], melhorIndividuoGeracaoAvaliada[1])
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

    agrupamentoGeracoes['geracao1'].sort(key=lambda item: funcaoTrelica(item[0], item[1]))
    agrupamentoGeracoes['geracao%d' % (idUltimaGeracaoComPopulacao)].sort(key=lambda item: funcaoTrelica(item[0], item[1]))

    melhorSolucaoG1 = agrupamentoGeracoes['geracao1'][0]
    print("-> Melhor solução para a primeira geração:")
    print("    Geração = %d" % 1)
    print("    X1 = %f e X2 = %f" % (melhorSolucaoG1[0], melhorSolucaoG1[1]))
    print("    f(x) = %.4f" % funcaoTrelica(melhorSolucaoG1[0], melhorSolucaoG1[1]))

    melhorSolucaoUltimaG = agrupamentoGeracoes['geracao%d' % (idUltimaGeracaoComPopulacao)][0]
    print("\n-> Melhor solução para a última geração:")
    print("    Geração = %d" % idUltimaGeracaoComPopulacao)
    print("    X1 = %f e X2 = %f" % (melhorSolucaoUltimaG[0], melhorSolucaoUltimaG[1]))
    print("    f(x) = %.4f" % funcaoTrelica(melhorSolucaoUltimaG[0], melhorSolucaoUltimaG[1]))

    print("\n-> Melhor solução geral considerando todas as gerações:")
    print("    Geração = %d" % geracaoMelhorSolucao)
    print("    X1 = %f e X2 = %f" % (individuoMelhorSolucao[0], individuoMelhorSolucao[1]))
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

def gerarAnaliseNExecucoesTrelica(N, qtdGeracoesMaxima, tamanhoPopulacaoInicial):

    listaIndividuos = []
    listaMelhoresSolucoes = []
    listaTemposExecucao = []
    
    for i in range(N):
        
        print("\n------------ ITERAÇÃO: %d ------------\n" % (i+1))

        individuoMelhorSolucao, melhorSolucao, tempoExecucao = problemaTrelica(qtdGeracoesMaxima, tamanhoPopulacaoInicial)

        listaIndividuos.append(individuoMelhorSolucao)
        listaMelhoresSolucoes.append(melhorSolucao)
        listaTemposExecucao.append(tempoExecucao)
    
    melhorIndice = listaMelhoresSolucoes.index(sorted(listaMelhoresSolucoes)[0])
    piorIndice = listaMelhoresSolucoes.index(sorted(listaMelhoresSolucoes)[-1])

    print("\n------------------------ RESULTADOS ------------------------\n\n")
    print("----- Problema da Treliça -----\n")
    print("Quantidade de iterações realizadas: %d" % N)
    print("Quantidade de gerações máxima: %d" % qtdGeracoesMaxima)
    print("Tamanho de população máximo: %d" % tamanhoPopulacaoInicial)
    print("Média das soluções: %f, Desvio Padrão das soluções: %f" % (statistics.mean(listaMelhoresSolucoes), statistics.stdev(listaMelhoresSolucoes)))
    print("Menor solução:")
    print("  X1 = %f" % listaIndividuos[melhorIndice][0])
    print("  X2 = %f" % listaIndividuos[melhorIndice][1])
    print("  f(x) = %f" % listaMelhoresSolucoes[melhorIndice])
    print("Maior solução:")
    print("  X1 = %f" % listaIndividuos[piorIndice][0])
    print("  X2 = %f" % listaIndividuos[piorIndice][1])
    print("  f(x) = %f" % listaMelhoresSolucoes[piorIndice])
    print("Média de tempo: %fs, Desvio padrão de tempo: %fs\n" % (statistics.mean(listaTemposExecucao), statistics.stdev(listaTemposExecucao)))
    print("------------------------------------------------------------\n")

gerarAnaliseNExecucoesTrelica(N=50, qtdGeracoesMaxima=1000, tamanhoPopulacaoInicial=1000)