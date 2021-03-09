# Импортируем главный класс программы
from view.Application import Application
# Импортируем модуль, для работы с операционной системой
import sys


# Точка входа в программу
if __name__ == "__main__":
    # Путь к файлу программы
    filePath = None
    # Если в параметрах командной строки есть аргумент, то присваиваем его переменной filePath
    if len(sys.argv) >= 2:
        filePath = sys.argv[1]

    # Создаём объект приложения. Передаём ему путь к файлу-проекту
    app = Application(filePath)
    # Запускаем цикл обработки событий
    app.mainloop()
