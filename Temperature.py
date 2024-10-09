import flet as ft


def main(page: ft.Page):
    page.title = "First task"  # налаштування сторінки
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.width = 350
    page.window.height = 450
    page.window.resizable = False
    page.window.maximizable = False

    temperature = ft.TextField(
        label="Enter temperature (°C)", width=250, text_align="center"  # поле для вводу температури
    )

    text = ft.Text("Waiting for temperature...")

    def get_temp(e):  # функція для отримання температури та виведення речень, відносто температури
        try:
            temp = float(temperature.value)
        except ValueError:
            text.value = "Enter a number"
            page.update()
            return

        if temp <= -100:
            text.value = "How have you not turned to ice yet?"
        elif -100 < temp <= -50:
            text.value = "Very cold."
        elif -50 < temp <= 0:
            text.value = "A cold, isn’t it?"
        elif 0 < temp < 10:
            text.value = "Cool."
        elif 10 < temp < 50:
            text.value = "Nice weather we’re having."
        elif 50 <= temp < 100:
            text.value = "Very hot."
        elif 100 <= temp:
            text.value = "How have you not melted yet?"
        page.update()

    def change_theme(e):  # функція для зміни теми (світла/темна)
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    button = ft.ElevatedButton(text="Confirm", on_click=get_temp)  # кнопочки
    theme_buttom = ft.IconButton(ft.icons.SUNNY, on_click=change_theme)

    page.add(
        ft.Row([text], alignment="center"),
        ft.Row([temperature], alignment="center"),  # сама сторінка
        ft.Row([button], alignment="center"),
        ft.Row([theme_buttom], alignment="center"),
    )


ft.app(target=main)
