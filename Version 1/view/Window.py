# Импортируем графическую библиотеку
from tkinter import *


# Базовое окно для создания всех дечерних окон
class Window(Frame):

    # Конструктор класса
    def __init__(self, parent, visible=False):
        # Вызываем конструктор базового класса
        super().__init__(parent)
        # Устанавливаем видимость окна
        self.setVisible(visible)
        # Настраиваем строки и столбцы окна
        self.tuneGrid()

    # Настроить строки и столбцы таблицы
    def tuneGrid(self):
        pass

    # Установить видимость окна
    def setVisible(self, value):
        if value:
            self.grid()
        else:
            self.grid_remove()