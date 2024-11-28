import flet as ft
from utils.pre_processamento_dados import PreProcessamentoDados
from view.home_screen import HomeScreen
from neural_network.neuronio import RedeNeural

def main(page: ft.Page):
    
    home = HomeScreen(page=page)

    # PreProcessamentoDados("treinamento.csv").print_dados()
    pre_processamento = PreProcessamentoDados("treinamento.csv")

    rede_neural = RedeNeural(
        n_entradas=pre_processamento.metadados.get("n_entradas"),
        n_saidas=pre_processamento.metadados.get("n_classes"),
        n_neuronios_intermed=pre_processamento.metadados.get("sugestao_n_neuronios_camada_oculta")
    )

    page.add(home.view)

    




ft.app(main)