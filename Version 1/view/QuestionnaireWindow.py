# Импортируем графическую библиотеку
from tkinter import *
from tkinter import ttk
# Импортируем базовое окно
from view.Window import Window


# Окно для добавления/редактирования/удаления вопросов
class QuestionnaireWindow(Window):

    def __init__(self, parent, visible=False):
        super().__init__(parent, visible=visible)

        # Поле для ввода вопроса
        self.entry = ttk.Entry(self)
        self.entry.grid(column=0, row=0, sticky=(E, W), pady=(10, 5), padx=10)

        # Список вопросов
        self.listBox = Listbox(self, font="Times 14")
        self.listBox.grid(column=0, row=1, rowspan=9, sticky=(N, S, E, W), pady=10, padx=10)

        # Прокрутка списка по оси x
        xScrollbar = Scrollbar(self, orient="horizontal")
        xScrollbar.config(command=self.listBox.xview)
        xScrollbar.grid(column=0, row=10, sticky=(N, S, E, W), padx=10)
        self.listBox.config(xscrollcommand=xScrollbar.set)

        # Прокрутка списка по оси y
        yScrollbar = Scrollbar(self, orient="vertical")
        yScrollbar.config(command=self.listBox.yview)
        yScrollbar.grid(column=1, row=1, rowspan=9, sticky=(S, N), pady=10)
        self.listBox.config(yscrollcommand=yScrollbar.set)

        # Кнопка Добавить новый вопрос
        self.addBtn = ttk.Button(self, text="Добавить")
        self.addBtn.grid(column=2, row=1, sticky=(N, S, E, W), pady=10, padx=10)

        # Кнопка изменить выбранный вопрос
        self.changeBtn = ttk.Button(self, text="Изменить")
        self.changeBtn.grid(column=2, row=2, sticky=(N, S, E, W), pady=10, padx=10)

        # Кнопка Удалить выделенный вопрос
        self.deleteBtn = ttk.Button(self, text="Удалить")
        self.deleteBtn.grid(column=2, row=3, sticky=(N, S, E, W), pady=10, padx=10)

        # Кнопка Поднять вопрос на позицию вверх
        self.upBtn = ttk.Button(self, text="Вверх")
        self.upBtn.grid(column=2, row=4, sticky=(N, S, E, W), pady=10, padx=10)

        # Кнопка Опустить вопрос на позицию вниз
        self.downBtn = ttk.Button(self, text="Вниз")
        self.downBtn.grid(column=2, row=5, sticky=(N, S, E, W), pady=10, padx=10)

    # Настроить параметры строк и столбцов
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=10)
        self.rowconfigure(4, weight=10)
        self.rowconfigure(5, weight=10)
        self.rowconfigure(6, weight=10)
        self.rowconfigure(7, weight=10)
        self.rowconfigure(8, weight=10)
        self.rowconfigure(9, weight=10)
        self.rowconfigure(10, weight=0)

    # Отчистить поля ввода
    def clear(self):
        self.entry.delete(0, END)
        self.listBox.delete(0, END)
