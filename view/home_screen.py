import flet as ft
from view.file_chooser import FileChooser
from utils.singleton import SingletonBase
from view.settings import Settings
from view.console import Console
class HomeScreen(SingletonBase):
    def __init__(self, page:ft.Page) -> None:


        self.file_chooser = FileChooser(page=page)
        self.settings = Settings(page=page)
        self.console = Console(page=page)

        self.view:ft.Control = ft.Container(ft.Column([
            ft.Text("Rede Neural com Backpropagation", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.file_chooser.view, 
                border=ft.Border(
                    top=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    right=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    bottom=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    left=ft.BorderSide(width=2, color=ft.colors.WHITE)
                ),
                border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15),
                width=page.window.width
            ),
            ft.Container(
                key="teste",
                content=self.settings.view, 
                border=ft.Border(
                    top=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    right=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    bottom=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    left=ft.BorderSide(width=2, color=ft.colors.WHITE)
                ),
                border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15)
            ),
            ft.Container(
                key="teste",
                content=self.console.view, 
                border=ft.Border(
                    top=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    right=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    bottom=ft.BorderSide(width=2, color=ft.colors.WHITE),
                    left=ft.BorderSide(width=2, color=ft.colors.WHITE)
                ),
                border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=20, bottom_right=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15),
                
            ),
            
        ], width=page.window.width, spacing=10), padding=ft.Padding(left=20, top=5, right=20, bottom=5))
        pass