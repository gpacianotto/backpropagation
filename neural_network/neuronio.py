import numpy as np
import pandas as pd
import copy

class Neuronio:
    def __init__(self, n:int, vies:float = 1.0):
        self.entradas:list[float] = np.zeros(n)
        self.pesos = np.random.rand(n)
        self.vies = vies
        self.n:float = n
        self.saida = 0
        pass

    def setEntrada(self, entrada:list[float]):
        if len(entrada) == len(self.entradas):
            self.entradas = copy.deepcopy(entrada)
    
    def calcSaida(self):
        net:float = 0
        
        for i in range(self.n):
           net = net + self.entradas[i]*self.pesos[i]
        
        net = net + self.vies

        self.saida = net

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

    def treinar(self, caminho_arquivo:str):
        # soon
        pass



rede = RedeNeural()