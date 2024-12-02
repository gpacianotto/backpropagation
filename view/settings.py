from utils.singleton import SingletonBase
import flet as ft
import re
from utils.interfaces import CondicaoParada, TipoCondicaoParada
from neural_network.neuronio import RedeNeural
from utils.pre_processamento_dados import PreProcessamentoDados

class Settings(SingletonBase):
    def __init__(self, page:ft.Page):
        
        self.page = page

        self.n_entradas = 0
        self.n_classes = 0
        self.sugestao_n_neuronios_camada_oculta = 0

        self.n_entradas_text = ft.Text(f"Número de Entradas: {self.n_entradas}")
        self.n_classes_text = ft.Text(f"Número de Classes: {self.n_classes}")

        self.input_funcao_ativacao = ft.Dropdown(
            label="Função de ativação",
            value="logistica",
            border_color=ft.colors.WHITE,
            options=[
                ft.dropdown.Option(text="Logística", key="logistica"),
                ft.dropdown.Option(text="Tangente Hiperbólica", key="tang_hiperbolica")
            ]
        )

        self.input_condicao_parada = ft.Dropdown(
            label="Condição de Parada",
            value=str(TipoCondicaoParada.NUM_INTERACOES),
            border_color=ft.colors.WHITE,
            options=[
                ft.dropdown.Option(text="Erro Máximo", key=str(TipoCondicaoParada.ERRO_MAXIMO)),
                ft.dropdown.Option(text="Nº Máximo de Iterações", key=str(TipoCondicaoParada.NUM_INTERACOES))
            ],
            on_change=self.on_change_dropdown_condicao_parada
        )

        self.input_n_neuronios_ocultos = ft.TextField(
            value=str(self.sugestao_n_neuronios_camada_oculta),
            label="Neuronios da camada oculta",
            hint_text="Insira apenas número inteiro",
            on_change=self.only_integer_mask,
            keyboard_type=ft.KeyboardType.NUMBER,  # Suggests numeric keyboard on mobile devices
            border_color=ft.colors.WHITE
        )

        self.input_erro_maximo = ft.TextField(
            value=str(0.001),
            label="Erro máximo",
            hint_text="Exemplo: 0.01",
            on_change=self.only_float_mask,
            keyboard_type=ft.KeyboardType.NUMBER,  # Suggests numeric keyboard on mobile devices,
            border_color=ft.colors.WHITE,
            disabled=True
        )

        self.input_n_iteracoes = ft.TextField(
            value=100,
            label="Número de Iterações",
            hint_text="Insira apenas número inteiro",
            on_change=self.only_integer_mask,
            keyboard_type=ft.KeyboardType.NUMBER,  # Suggests numeric keyboard on mobile devices
            border_color=ft.colors.WHITE
        )

        self.input_taxa_aprendizado = ft.TextField(
            value=str(0.1),
            label="Taxa de aprendizado",
            hint_text="Exemplo: 0.01",
            on_change=self.only_float_mask,
            keyboard_type=ft.KeyboardType.NUMBER,  # Suggests numeric keyboard on mobile devices,
            border_color=ft.colors.WHITE
        )

        self.treinar_e_testar_rede_button = ft.FilledButton("Treinar e Testar Rede", on_click=self.train_and_test_network)

        self.view = ft.Column([
            ft.Row([
                self.n_entradas_text,
                self.n_classes_text,
                ft.Text(""),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                self.input_funcao_ativacao,
                self.input_taxa_aprendizado,
                self.input_n_neuronios_ocultos
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                self.input_condicao_parada,
                self.input_erro_maximo,
                self.input_n_iteracoes
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.treinar_e_testar_rede_button
        ], spacing=20)
        pass
    
    def train_and_test_network(self, e):
        self.treinar_e_testar_rede_button.disabled = True
        self.page.update()
        
        condicao_parada = None

        if self.input_condicao_parada.value == "TipoCondicaoParada.ERRO_MAXIMO":
            condicao_parada = CondicaoParada(tipo=TipoCondicaoParada.ERRO_MAXIMO, value=float(self.input_erro_maximo.value))
        else:
            condicao_parada = CondicaoParada(tipo=TipoCondicaoParada.NUM_INTERACOES, value=int(self.input_n_iteracoes.value))

        rede_neural = RedeNeural(
            n_entradas=self.n_entradas,
            n_saidas=self.n_classes,
            n_neuronios_intermed=int(self.input_n_neuronios_ocultos.value),
            condicao_parada=condicao_parada,
            funcao_transf=self.input_funcao_ativacao.value,
            taxa_aprendizado=float(self.input_taxa_aprendizado.value)
        )

        rede_neural.treinar(PreProcessamentoDados())
        rede_neural.testar(PreProcessamentoDados())

        self.treinar_e_testar_rede_button.disabled = False
        self.page.update()
        pass

    def only_integer_mask(self, e:ft.ControlEvent):
        # Regex to match integer numbers (positive or negative)
        if not re.fullmatch(r"-?\d*", e.control.value):
            e.control.error_text = "Apenas números inteiros são permitidos"
        else:
            e.control.error_text = None
        e.control.update()
    
    def only_float_mask(self, e:ft.ControlEvent):
        # Regex to match floating-point numbers (positive or negative)
        if not re.fullmatch(r"-?\d*(\.\d*)?", e.control.value):
            try:
                float(e.control.value)
            except ValueError:
                e.control.error_text = "O valor deve ser Float"
        else:
            if float(e.control.value) < 0.0 or float(e.control.value) > 1.0:
                e.control.error_text = "Deve estar entre 0.0 e 1.0"
            else:
                e.control.error_text = None
        e.control.update()

    def on_change_dropdown_condicao_parada(self, e):
        # print(e.control.value)
        if e.control.value == "TipoCondicaoParada.ERRO_MAXIMO":
            self.input_n_iteracoes.disabled = True
            self.input_erro_maximo.disabled = False
        elif e.control.value == "TipoCondicaoParada.NUM_INTERACOES":
            self.input_n_iteracoes.disabled = False
            self.input_erro_maximo.disabled = True
        self.page.update()

    def update_n_entradas(self, n_entradas:int):
        
        self.n_entradas = n_entradas
        self.n_entradas_text.value = f"Número de Entradas: {self.n_entradas}"
        self.page.update()

    def update_n_classes(self, n_classes:int):
        
        self.n_classes = n_classes
        self.n_classes_text.value = f"Número de Classes: {self.n_classes}"
        self.page.update()

    def update_n_neuronios_camada_oculta(self, n_neuronios:int):
        
        self.sugestao_n_neuronios_camada_oculta = n_neuronios
        # self.sugestao_n_neuronios_camada_oculta_text.value = f"Número de neuronios da camada oculta: {self.sugestao_n_neuronios_camada_oculta}"
        self.input_n_neuronios_ocultos.value = str(n_neuronios)
        self.page.update()