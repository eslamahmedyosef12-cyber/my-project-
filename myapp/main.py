import flet as ft

def main(page: ft.Page):
    page.title = "بوتاتي الشامل"
    page.add(ft.Text("أهلاً بك في تطبيقي الأول!"))

ft.app(target=main)

