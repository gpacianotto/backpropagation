import flet as ft
from utils.singleton import SingletonBase

class Console(SingletonBase):
    def __init__(self, page:ft.Page = None):

        if page == None:
            return

        self.page = page

        self.view = ft.Column([
            ft.Text("CONSOLE INICIADO COM SUCESSO!")
        ], 
        width=page.window.width,
        height=200,
        on_scroll_interval=0,
        scroll=ft.ScrollMode.ALWAYS
        )
    
    def printOnConsole(self, s:str):
        self.view.controls.insert(0, ft.Text(s))
        self.page.update()

    def editFirstLine(self, s:str):
        self.view.controls[0] = ft.Text(s)
        self.page.update()