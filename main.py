from functions import MainFunctions
import flet as ft

def main(page: ft.Page):
    page.title = "File Storage Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Обработчик для загрузки файла
    def upload_file(e):
        if file_picker.result and file_picker.result.files:
            file_path = file_picker.result.files[0].path
            filename = file_path.split('/')[-1]
            with open(file_path, 'rb') as f:
                file_data = f.read()
            MainFunctions.add_file(filename, file_data)
            refresh_file_list()
            page.snack_bar = ft.SnackBar(ft.Text(f"Файл '{filename}' успешно загружен!"))
            page.snack_bar.open = True
            page.update()

    # Обновление списка файлов
    def refresh_file_list(search_query=None):
        files = MainFunctions.show_files()
        file_list.controls.clear()
        for file_id, filename in files:
            # Фильтрация по поисковому запросу
            if search_query and search_query.lower() not in filename.lower():
                continue
            file_list.controls.append(
                ft.ListTile(
                    title=ft.Text(filename),
                    trailing=ft.IconButton(
                        icon=ft.icons.DOWNLOAD,
                        tooltip="Скачать файл",
                        on_click=lambda e, id=file_id, name=filename: download_file(id, name)
                    ),
                    shape=ft.RoundedRectangleBorder(radius=5),
                    bgcolor=ft.colors.LIGHT_BLUE_50,
                    content_padding=10
                )
            )
        page.update()

    # Функция для скачивания файла
    def download_file(file_id, filename):
        file = MainFunctions.get_file(file_id)
        if file:
            with open(f"downloaded_{filename}", 'wb') as f:
                f.write(file[0])
            page.snack_bar = ft.SnackBar(ft.Text(f"Файл '{filename}' успешно скачан!"))
            page.snack_bar.open = True
            page.update()

    # Обработчик поиска файлов
    def search_files(e):
        search_query = search_box.value
        refresh_file_list(search_query)

    # Инициализация элементов интерфейса
    file_picker = ft.FilePicker(on_result=upload_file)
    upload_button = ft.ElevatedButton(
        text="Загрузить файл",
        icon=ft.icons.UPLOAD_FILE,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_ACCENT,
            padding=10,
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        on_click=lambda _: file_picker.pick_files()
    )

    search_box = ft.TextField(
        hint_text="Введите имя файла для поиска",
        on_change=search_files,
        expand=True
    )
    search_button = ft.IconButton(
        icon=ft.icons.SEARCH,
        tooltip="Найти файл",
        on_click=search_files,
        bgcolor=ft.colors.BLUE_ACCENT,
        icon_color=ft.colors.WHITE
    )

    file_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    # Добавление элементов на страницу
    page.add(
        ft.Row([upload_button, file_picker], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row([search_box, search_button], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        ft.Divider(height=20, thickness=1),
        file_list
    )

    # Первоначальная загрузка списка файлов
    refresh_file_list()

# Запуск приложения
ft.app(target=main)
