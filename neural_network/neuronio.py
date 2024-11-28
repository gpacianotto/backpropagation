import numpy as np
import pandas as pd
import copy
from utils.pre_processamento_dados import PreProcessamentoDados

class Neuronio:
    def __init__(self, n:int, vies:float = 1.0):
        self.entradas:list[float] = np.zeros(n)
        self.pesos = np.random.rand(n)
        self.vies = vies
        self.n:float = n
        self.net = 0
        pass

    def setEntrada(self, entrada:list[float]):
        if len(entrada) == len(self.entradas):
            self.entradas = copy.deepcopy(entrada)
    
    def calcNet(self):
        net:float = 0
        
        for i in range(self.n):
           net = net + self.entradas[i]*self.pesos[i]
        
        net = net + self.vies

        self.net = net
    
    def aplicaFuncao(self):
        pass

class RedeNeural:
    def __init__(self,n_entradas:int, n_saidas:int, n_neuronios_intermed:int):
        
        self.camada_entrada:list[Neuronio] = []
        self.camada_intermediaria: list[Neuronio] = []
        self.camada_saida:list[Neuronio] = []

        for i in range(n_entradas):
            self.camada_entrada.append(Neuronio(1))
        
        for i in range(n_neuronios_intermed):
            self.camada_intermediaria.append(Neuronio(n_entradas))
        
        for i in range(n_saidas):
            self.camada_saida.append(Neuronio(n_neuronios_intermed))
        pass

    def treinar(self, metadata:PreProcessamentoDados):
        # soon
        entradas = []
        for index, row in metadata.data.iterrows():
            # print(f"Row {index + 1}: {row.to_dict()}")
            dado_entrada = row.to_dict()

            for i in range(metadata.metadados.get("n_entradas")):
                entradas.append(float(dado_entrada.get("X" + str(i+1))))
                pass
            
            for i in range(entradas):
                self.camada_entrada[i].setEntrada([entradas[i]])
                self.camada_entrada[i].calcNet()

            
            entradas = []

        pass



# rede = RedeNeural()