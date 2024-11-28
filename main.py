import flet as ft
from utils.pre_processamento_dados import PreProcessamentoDados

def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))

    # PreProcessamentoDados("treinamento.csv").print_dados()
    PreProcessamentoDados("treinamento.csv").extrair_info_dados()



ft.app(main)