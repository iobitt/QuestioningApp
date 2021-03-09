# Импортируем графическую библиотеку
from tkinter import *
from tkinter import ttk
# Импортируем базовое окно
from view.Window import Window
# Импортируем окно для проведения анализа опроса
from view.AnalysisWindow import AnalysisWindow


# Окно для представления результатов опроса
class SurveyViewWindow(Window):

    # Конструктор класса
    def __init__(self, parent, visible=False):
        # Вызываем конструктор базового класса
        super().__init__(parent, visible=visible)

        # Таблица для отображения вопросов и ответов
        self.tree = ttk.Treeview(self)
        # Размещаем элемент на сетку окна
        self.tree.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W), pady=10, padx=10)

        # Прокрутка таблицы по оси x
        self.xScrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.xScrollbar.grid(column=0, row=1, columnspan=2, sticky=(E, W))
        self.tree.configure(xscrollcommand=self.xScrollbar.set)

        # Прокрутка таблицы по оси y
        self.yScrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.yScrollbar.grid(column=2, row=0, sticky=(N, S))
        self.tree.configure(yscrollcommand=self.yScrollbar.set)

        # Окно для анализа опроса
        self.analysisWindow = AnalysisWindow(self)
        self.analysisWindow.grid(column=3, row=0, sticky=(N, S, E, W), pady=10, padx=10)

        # Кнопка для сортировки ответов по выбранному вопросу
        self.sortBtn = ttk.Button(self, text="Отсортировать")
        self.sortBtn.grid(column=1, row=2, sticky=(N, S, E, W), pady=10, padx=10)

    # Настроить параметры строк и столбцов таблицы
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=20)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=95)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=5)
