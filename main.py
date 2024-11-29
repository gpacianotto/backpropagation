import flet as ft
from utils.pre_processamento_dados import PreProcessamentoDados
from view.home_screen import HomeScreen
from neural_network.neuronio import RedeNeural

def main(page: ft.Page):
    
    home = HomeScreen(page=page)
    

    # PreProcessamentoDados("treinamento.csv").print_dados()
    pre_processamento = PreProcessamentoDados("dummie.csv")

    rede_neural = RedeNeural(
        n_entradas=int(pre_processamento.metadados.get("n_entradas")),
        n_saidas=int(pre_processamento.metadados.get("n_classes")),
        n_neuronios_intermed=int(pre_processamento.metadados.get("sugestao_n_neuronios_camada_oculta")),
        funcao_transf="tang_hiperbolica"
    )

    rede_neural.treinar(pre_processamento)

    page.add(home.view)

    




ft.app(main)