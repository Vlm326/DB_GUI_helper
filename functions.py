from psycopg2 import connect, Binary

class MainFunctions:
    @staticmethod
    def connect_database():
        try:
            connection = connect(
                dbname='file_storage',
                user='vlm326',
                password='123690',
                host='localhost',
                port='5432'
            )
            print("Подключение успешно")
            return connection
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None

    @staticmethod
    def add_file(filename, file_data):
        con = MainFunctions.connect_database()
        if con:
            try:
                with con:
                    with con.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO files (filename, file_data) VALUES (%s, %s)",
                            (filename, Binary(file_data))
                        )
                print(f"Файл '{filename}' успешно добавлен.")
            except Exception as e:
                print(f"Ошибка при добавлении файла: {e}")
            finally:
                con.close()

    @staticmethod
    def show_files():
        con = MainFunctions.connect_database()
        if con:
            try:
                with con:
                    with con.cursor() as cursor:
                        cursor.execute("SELECT id, filename FROM files")
                        files = cursor.fetchall()
                return files
            except Exception as e:
                print(f"Ошибка при получении списка файлов: {e}")
                return []
            finally:
                con.close()

    @staticmethod
    def get_file(file_id):
        con = MainFunctions.connect_database()
        if con:
            try:
                with con:
                    with con.cursor() as cursor:
                        cursor.execute("SELECT file_data FROM files WHERE id=%s", (file_id,))
                        file = cursor.fetchone()
                return file
            except Exception as e:
                print(f"Ошибка при получении файла: {e}")
                return None
            finally:
                con.close()
