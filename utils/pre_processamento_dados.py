import pandas as pd
import re
import math
from itertools import zip_longest

class PreProcessamentoDados:
    def __init__(self, caminho_arquivo:str, caminho_arquivo_teste:str):
        
        self.data:pd.DataFrame = pd.read_csv(caminho_arquivo)

        # embaralhando os dados em ordem aleatória
        self.data = self.data.sample(frac=1).reset_index(drop=True)

        # normalizando dados
        for col in self.data.columns:
            if re.match(r"^X\d+$", col):
                self.data[col] = (self.data[col] - self.data[col].min())/(self.data[col].max() - self.data[col].min())

        self.data_teste = pd.read_csv(caminho_arquivo_teste)

        self.data_teste = self.data_teste.sample(frac=1).reset_index(drop=True)

        for col in self.data_teste.columns:
            if re.match(r"^X\d+$", col):
                self.data_teste[col] = (self.data_teste[col] - self.data_teste[col].min())/(self.data_teste[col].max() - self.data_teste[col].min())

        self.extrair_info_dados()
        pass

    def print_dados(self):
        for index, row in self.data.iterrows():
            print(f"Row {index + 1}: {row.to_dict()}")
    
    def split_dataframe_by_column(self, column_name):
        dataframes = {}
        unique_values = self.data[column_name].unique()
        for value in unique_values:
            dataframes[value] = self.data[self.data[column_name] == value]
        return dataframes

    def extrair_info_dados(self):
        colunas = self.data.columns

        n_entradas = 0

        for col in colunas:
            if re.match(r"^X\d+$", col):
                n_entradas += 1
        
        classes = {}

        for index, row in self.data.iterrows():
            classe = row.get("classe")
            
            if classes.get(classe) == None:
                classes[classe] = 1
            else:
                classes[classe] += 1
        
        n_classes = len(classes.keys())

        sugestao_n_neuronios_camada_oculta = math.ceil(math.sqrt(n_entradas * n_classes))

        result = {
            "n_entradas": n_entradas,
            "colunas": colunas,
            "classes": classes,
            "n_classes": n_classes,
            "sugestao_n_neuronios_camada_oculta": sugestao_n_neuronios_camada_oculta
        }
        # print(result)
        # return result
        self.metadados = result