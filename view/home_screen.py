import flet as ft

class HomeScreen:
    def __init__(self, page:ft.Page) -> None:
        self.view:ft.Control = ft.Row([
            ft.Column([
                ft.Text("Arquivo de treinamento escolhido: N/A"),
                ft.FilledButton(text="Escolher arquivo de treinamento"),
                ft.Text("Arquivo de teste escolhido: N/A"),
                ft.FilledButton(text="Escolher arquivo de teste")
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        height=page.window.height
        )
        pass