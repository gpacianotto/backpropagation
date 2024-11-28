import flet as ft
from utils.pre_processamento_dados import PreProcessamentoDados
from view.home_screen import HomeScreen

def main(page: ft.Page):
    
    home = HomeScreen(page=page)

    # PreProcessamentoDados("treinamento.csv").print_dados()
    # PreProcessamentoDados("treinamento.csv").extrair_info_dados()

    page.add(home.view)

    




ft.app(main)