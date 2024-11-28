import pandas as pd
import re
from itertools import zip_longest

class PreProcessamentoDados:
    def __init__(self, caminho_arquivo):
        
        self.data = pd.read_csv(caminho_arquivo)
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

        splitDfs = self.split_dataframe_by_column("classe")

        for key, dataframe in splitDfs.items():
            dataframe.to_csv(str(key) + ".csv")
        
        

        result = {
            "n_entradas": n_entradas,
            "colunas": colunas,
            "classes": classes,
            "n_classes": n_classes
        }
        print(result)
        return result