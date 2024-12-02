import flet as ft
from utils.singleton import SingletonBase
from utils.pre_processamento_dados import PreProcessamentoDados
from view.settings import Settings

class FileChooser(SingletonBase):
    def __init__(self, page:ft.Page) -> None:

        self.page = page

        self.button_train_file = ft.FilledButton(text="Escolher arquivo de treinamento", on_click=self.on_click_train)
        self.text_train_file = ft.Text("Arquivo de treinamento escolhido: N/A")

        self.button_test_file = ft.FilledButton(text="Escolher arquivo de teste", on_click=self.on_click_test)
        self.text_test_file = ft.Text("Arquivo de teste escolhido: N/A")


        self.pick_files_dialog_train = ft.FilePicker(on_result=self.pick_files_result_train)
        self.pick_files_dialog_test = ft.FilePicker(on_result=self.pick_files_result_test)

        self.caminho_arquivo_treino = ""
        self.caminho_arquivo_teste = ""
        self.metadados = None

        self.view:ft.Control = ft.Column([
            ft.Row([
                ft.Row([
                    ft.Column([
                        self.button_train_file,
                        self.text_train_file,
                        self.pick_files_dialog_train,
                    ], alignment=ft.MainAxisAlignment.START)
                ]),
                ft.Row([
                    ft.Column([
                        self.button_test_file,
                        self.text_test_file,
                        self.pick_files_dialog_test
                    ], alignment=ft.MainAxisAlignment.START)

                ]),
            
            
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            height=70
            ),
            ft.Row([
                ft.FilledButton("Processar arquivos", on_click=self.on_click_comecar_analise)
            ],alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
        pass
    
    def on_click_comecar_analise(self, e):
        if self.caminho_arquivo_treino != "" and self.caminho_arquivo_teste != "":
            self.metadados = PreProcessamentoDados(caminho_arquivo=self.caminho_arquivo_treino, caminho_arquivo_teste=self.caminho_arquivo_teste)
            settings = Settings(self.page)
            settings.update_n_classes(int(self.metadados.metadados["n_classes"]))
            settings.update_n_entradas(int(self.metadados.metadados["n_entradas"]))
            settings.update_n_neuronios_camada_oculta(int(self.metadados.metadados["sugestao_n_neuronios_camada_oculta"]))
            pass 
        pass

    def on_click_train(self, e):
        self.pick_files_dialog_train.pick_files("Escolha o seu arquivo de treino")
        pass

    def pick_files_result_train(self, e:ft.FilePickerResultEvent):
        
        self.caminho_arquivo_treino = e.files[0].path
        
        self.text_train_file.value = f"Arquivo de treino escolhido: {e.files[0].name}"
        
        self.page.update()
        pass


    def on_click_test(self, e):
        self.pick_files_dialog_test.pick_files("Escolha o seu arquivo de testes")
        pass

    def pick_files_result_test(self, e:ft.FilePickerResultEvent):
        print(f"arquivo escolhido {e.files[0]}")

        self.caminho_arquivo_teste = e.files[0].path

        self.text_test_file.value = f"Arquivo de teste escolhido: {e.files[0].name}"
        self.page.update()
        pass