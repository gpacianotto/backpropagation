import numpy as np
import pandas as pd
import math
import copy
from utils.pre_processamento_dados import PreProcessamentoDados
from utils.interfaces import CondicaoParada, TipoCondicaoParada

class Neuronio:
    def __init__(self, n:int):
        self.entradas:list[float] = np.zeros(n)
        self.pesos = np.random.rand(n)
        self.n:float = n
        self.net = 0
        self.saida = 0

        logistica = lambda x: 1 /(1+ (math.e ** (-x)) )
        tang_hiperbolica = lambda x: (1 - math.e ** (-2 * x)) / (1 + math.e ** (-2 * x))

        self.funcoes = {
            "logistica": {
                "value": logistica,
                "derivate": lambda x: logistica(x) * (1 - logistica(x))
            },
            "tang_hiperbolica": {
                "value": tang_hiperbolica,
                "derivate": lambda x: 1 - tang_hiperbolica(x) ** 2
            }
        }
        pass

    def setEntrada(self, entrada:list[float]):
        
        self.entradas = copy.deepcopy(entrada)
    
    def calcNet(self):
        net:float = 0
        
        for i in range(self.n):
           net = net + self.entradas[i]*self.pesos[i]
        # print("new net: ", net)
        self.net = net
    
    def aplicaFuncao(self, funcao:str):
        self.saida = self.funcoes[funcao]["value"](self.net)

    def aplicaDerivada(self, funcao:str):
        return self.funcoes[funcao]["derivate"](self.net)

class RedeNeural:
    def __init__(self,n_entradas:int, n_saidas:int, n_neuronios_intermed:int, funcao_transf:str, taxa_aprendizado:float=0.5, condicao_parada:CondicaoParada=CondicaoParada(TipoCondicaoParada.NUM_INTERACOES, 800)):
        np.set_printoptions(legacy='1.25')
        self.camada_entrada:list[Neuronio] = []
        self.camada_intermediaria: list[Neuronio] = []
        self.camada_saida:list[Neuronio] = []
        self.funcao_trasnf = funcao_transf
        self.taxa_aprendizado = taxa_aprendizado
        self.condicao_parada = condicao_parada

        for i in range(n_entradas):
            self.camada_entrada.append(Neuronio(1))
        
        for i in range(n_neuronios_intermed):
            self.camada_intermediaria.append(Neuronio(n_entradas))
        
        for i in range(n_saidas):
            self.camada_saida.append(Neuronio(n_neuronios_intermed))
        pass
    
    # def forward_pass(self, entrada: list[float]) -> list[float]:
    #     """Realiza a propagação para frente na rede neural."""
    #     # Propagação camada intermediária
    #     for neuronio in self.camada_intermediaria:
    #         neuronio.setEntrada(copy.deepcopy(entrada))
    #         neuronio.calcNet()
    #         neuronio.aplicaFuncao(self.funcao_trasnf)
        
    #     # Saídas da camada intermediária
    #     entradas_intermediaria = [neuronio.saida for neuronio in self.camada_intermediaria]

    #     # Propagação camada de saída
    #     for neuronio in self.camada_saida:
    #         neuronio.setEntrada(copy.deepcopy(entradas_intermediaria))
    #         neuronio.calcNet()
    #         neuronio.aplicaFuncao(self.funcao_trasnf)
        
    #     # Saídas da camada de saída
    #     return [neuronio.saida for neuronio in self.camada_saida]


    # def treinar(self, metadata: PreProcessamentoDados, epochs: int = 1000, taxa_aprendizado: float = 0.01, regularizacao: float = 0.001, batch_size: int = 32):
    #     """
    #     Treina a rede neural usando o algoritmo defor col in self.data.columns:
    #         metadata (PreProcessamentoDados): Dados pré-processados para o treinamento.
    #         epochs (int): Número de épocas para o treinamento.
    #         taxa_aprendizado (float): Taxa de aprendizado inicial.
    #         regularizacao (float): Fator de regularização L2 para evitar overfitting.
    #         batch_size (int): Tamanho dos lotes (minibatches) usados no treinamento.
    #     """
    #     for epoch in range(epochs):
    #         erro_total = 0
    #         # Embaralhar os dados para cada época
    #         dados_embaralhados = metadata.data.sample(frac=1).reset_index(drop=True)
            
    #         # Dividir os dados em minibatches
    #         for inicio in range(0, len(dados_embaralhados), batch_size):
    #             batch = dados_embaralhados.iloc[inicio:inicio + batch_size]
                
    #             gradientes_saida = [np.zeros_like(neuronio.pesos) for neuronio in self.camada_saida]
    #             gradientes_intermediaria = [np.zeros_like(neuronio.pesos) for neuronio in self.camada_intermediaria]
                
    #             for _, row in batch.iterrows():
    #                 dado_entrada = row.to_dict()
                    
    #                 # Preparação dos dados de entrada e saída esperada
    #                 entrada = [float(dado_entrada.get(f"X{i+1}")) for i in range(metadata.metadados["n_entradas"])]
    #                 saida_esperada = dado_entrada.get("classe")

    #                 # Normalização (opcional, dependendo dos dados)
    #                 entrada = np.array(entrada) / np.max(np.abs(entrada))

    #                 # Propagação para frente
    #                 saida = self.forward_pass(entrada)

    #                 # Cálculo do erro total
    #                 erro_total += sum((saida_esperada[i] - saida[i]) ** 2 for i in range(len(saida_esperada)))

    #                 # Retropropagação do erro
    #                 erros_saida = [
    #                     saida_esperada[i] - self.camada_saida[i].saida
    #                     for i in range(len(saida_esperada))
    #                 ]
                    
    #                 # Gradientes da camada de saída
    #                 for i, neuronio in enumerate(self.camada_saida):
    #                     gradiente = erros_saida[i] * self.funcoes[self.funcao_trasnf]["derivate"](neuronio.net)
    #                     for j in range(len(neuronio.pesos)):
    #                         gradientes_saida[i][j] += gradiente * self.camada_intermediaria[j].saida

    #                 # Erros na camada intermediária
    #                 erros_intermediaria = [
    #                     sum(
    #                         erros_saida[k] * self.camada_saida[k].pesos[i]
    #                         for k in range(len(self.camada_saida))
    #                     )
    #                     for i in range(len(self.camada_intermediaria))
    #                 ]

    #                 # Gradientes da camada intermediária
    #                 for i, neuronio in enumerate(self.camada_intermediaria):
    #                     gradiente = erros_intermediaria[i] * self.funcoes[self.funcao_trasnf]["derivate"](neuronio.net)
    #                     for j in range(len(neuronio.pesos)):
    #                         gradientes_intermediaria[i][j] += gradiente * entrada[j]
                
    #             # Atualização dos pesos com regularização L2
    #             for i, neuronio in enumerate(self.camada_saida):
    #                 neuronio.pesos += taxa_aprendizado * (gradientes_saida[i] / batch_size - regularizacao * neuronio.pesos)
                
    #             for i, neuronio in enumerate(self.camada_intermediaria):
    #                 neuronio.pesos += taxa_aprendizado * (gradientes_intermediaria[i] / batch_size - regularizacao * neuronio.pesos)

    #         # Diminuição da taxa de aprendizado (opcional)
    #         taxa_aprendizado *= 0.99

    #         # Exibir progresso a cada 100 épocas
    #         if epoch % 100 == 0:
    #             print(f"Época {epoch}/{epochs} - Erro Total: {erro_total}")

    def treinar(self, metadata:PreProcessamentoDados):
        entradas = []
        entradas_camada_saida = []
        saida = []
        erroSaida = []
        erroIntermed = []
        n_classes = int(metadata.metadados.get("n_classes"))
        saidas_esperadas= np.zeros(n_classes)

        n_iter = 0

        erro_rede_final = 0

        while True:


            for index, row in metadata.data.iterrows():
                # print(f"Row {index + 1}: {row.to_dict()}")
                dado_entrada = row.to_dict()

                for i in range(metadata.metadados.get("n_entradas")):
                    entradas.append(float(dado_entrada.get("X" + str(i+1))))
                    pass
                
                classe_esperada = int(dado_entrada.get("classe"))
                saidas_esperadas[classe_esperada - 1] = 1
                # print("saidas esperadas: ", saidas_esperadas.tolist())
                # print("entrada: ", entradas)

                for neuronio in self.camada_intermediaria:
                    neuronio.setEntrada(entrada=copy.deepcopy(entradas))
                for neuronio in self.camada_intermediaria:
                    neuronio.calcNet()
                for neuronio in self.camada_intermediaria:
                    neuronio.aplicaFuncao(self.funcao_trasnf)
                for neuronio in self.camada_intermediaria:
                    entradas_camada_saida.append(neuronio.saida)

                # print("intermed: ", entradas_camada_saida)

                for neuronio in self.camada_saida:
                    neuronio.setEntrada(copy.deepcopy(entradas_camada_saida))
                for neuronio in self.camada_saida:
                    neuronio.calcNet()
                for neuronio in self.camada_saida:    
                    neuronio.aplicaFuncao(self.funcao_trasnf)
                for neuronio in self.camada_saida:    
                    saida.append(neuronio.saida)
                
                # print("saida: ",saida)

                # calcular o erro na camada de saida
                for i in range(len(self.camada_saida)):
                    deriv = self.camada_saida[i].aplicaDerivada(self.funcao_trasnf)
                    erroSaida.append((saidas_esperadas[i] - saida[i]) * (deriv))
                
                # calcular o erro na camada intermediaria
                
                for i in range(len(self.camada_intermediaria)):
                    deriv = self.camada_intermediaria[i].aplicaDerivada(self.funcao_trasnf)
                    
                    somatorio = 0

                    for j in range(len(self.camada_saida)):
                        somatorio += erroSaida[j] * self.camada_saida[j].pesos[i]

                    erroIntermed.append(deriv * somatorio)
                
                # atualiza os pesos da camada de saída
                # n do slide = taxa de aprendizado
                for n in range(len(self.camada_saida)):
                    for i in range(len(self.camada_saida[n].pesos)):
                        self.camada_saida[n].pesos[i] += self.taxa_aprendizado * erroSaida[n] * self.camada_saida[n].entradas[i]
                
                # atualiza os pesos da camada intermediaria
                # n do slide = taxa de aprendizado
                for n in range(len(self.camada_intermediaria)):
                    for i in range(len(self.camada_intermediaria[n].pesos)):
                        self.camada_intermediaria[n].pesos[i] += self.taxa_aprendizado * erroIntermed[n] * self.camada_intermediaria[n].entradas[i]
                
                # calcular erro da rede

                erro_rede = 0

                for erro in erroSaida:
                    erro_rede += erro ** 2
                
                erro_rede = erro_rede / 2

                erro_rede_final = erro_rede

                
                # TCHU DU: PASSAR O CALCULO DO ERRO DA REDE PARA FORA DESSE FOR
                 

                entradas.clear()
                entradas_camada_saida.clear()
                saida.clear()
                erroSaida.clear()
                erroIntermed.clear()
                saidas_esperadas= np.zeros(n_classes)
            
            if self.condicao_parada.tipo == TipoCondicaoParada.ERRO_MAXIMO and erro_rede_final <= self.condicao_parada.value:
                print(f"Condição de parada atingida! Erro máximo permitido = {self.condicao_parada.value} erro obtido pela rede = {erro_rede}")
                break
            elif self.condicao_parada.tipo == TipoCondicaoParada.NUM_INTERACOES and (n_iter + 1) >= self.condicao_parada.value:
                print(f"Condição de parada atingida! Número de iterações atingido: {n_iter + 1} -> {self.condicao_parada.value}")
                break
            
            print(f"iteração {n_iter} -> erro da rede: {erro_rede_final}")
            n_iter += 1

            pass

    def testar(self, metadata:PreProcessamentoDados):

        entradas = []
        entradas_camada_saida = []
        saida = []
        matriz_de_confusao = []
        
        n_classes = metadata.metadados.get("n_classes")

        for i in range(n_classes):
            buffer = []
            for j in range(n_classes):
                buffer.append(0)
            matriz_de_confusao.append(buffer)

        for index, row in metadata.data_teste.iterrows():
            dado_entrada = row.to_dict()

            for i in range(metadata.metadados.get("n_entradas")):
                entradas.append(float(dado_entrada.get("X" + str(i+1))))
                pass
            
            classe_esperada = int(dado_entrada.get("classe"))
            # saidas_esperadas[classe_esperada - 1] = 1
                
            print("entrada: ", entradas)

            for neuronio in self.camada_intermediaria:
                neuronio.setEntrada(entrada=copy.deepcopy(entradas))
            for neuronio in self.camada_intermediaria:
                neuronio.calcNet()
            for neuronio in self.camada_intermediaria:
                neuronio.aplicaFuncao(self.funcao_trasnf)
            for neuronio in self.camada_intermediaria:
                entradas_camada_saida.append(neuronio.saida)

            # print("intermed: ", entradas_camada_saida)

            for neuronio in self.camada_saida:
                neuronio.setEntrada(copy.deepcopy(entradas_camada_saida))
            for neuronio in self.camada_saida:
                neuronio.calcNet()
            for neuronio in self.camada_saida:    
                neuronio.aplicaFuncao(self.funcao_trasnf)
            for neuronio in self.camada_saida:    
                saida.append(neuronio.saida)
            
            print("saida: ", saida)
            
            # # ENCONTRANDO INDEX 
            index_maior_elemento = 0    
            maior_elemento = saida[index_maior_elemento]

            for i in range (len(saida)): 
                if saida[i] > maior_elemento: 
                    maior_elemento = saida[i]
                    index_maior_elemento = i
            
            matriz_de_confusao[classe_esperada - 1][index_maior_elemento] += 1

            entradas_camada_saida.clear()
            saida.clear()
            entradas.clear()
        print("matriz de confusao: ", matriz_de_confusao)
        pass



# rede = RedeNeural()