from tkinter import *
from tkinter import ttk
from view.Window import Window


# Окно для проведения анализа опроса
class AnalysisWindow(Window):
    
    def __init__(self, parent, visible=False):
        super().__init__(parent, visible=visible)

        # Метка Возраст
        self.ageLbl = Label(self, text="Возраст")
        self.ageLbl.grid(column=0, row=0, padx=5, pady=(5, 5))
        
        # Поле для выбора неравенства для возраста
        self.ageInequality = ttk.Combobox(self, values=["больше", "меньше"], state='readonly')
        self.ageInequality.grid(column=0, row=1, padx=5, pady=(0, 5))
        self.ageInequality.current(1)
        
        # Поля для выбора возраста
        self.age = ttk.Combobox(self, values=[i for i in range(0, 150)], state='readonly')
        self.age.grid(column=0, row=2, padx=5, pady=5)
        self.age.current(1)
        
        # Метка пол
        self.genderLbl = Label(self, text="Пол")
        self.genderLbl.grid(column=0, row=3, padx=5, pady=(10, 5))
        
        # Поле для выбора пола
        self.gender = ttk.Combobox(self, values=["мужской", "женский"], state='readonly')
        self.gender.grid(column=0, row=4, padx=5, pady=(0, 5))
        
        # Метка образование
        self.educationLbl = Label(self, text="Образование")
        self.educationLbl.grid(column=0, row=5, padx=5, pady=(10, 5))
        
        # Поле для выбора образования
        self.education = ttk.Combobox(self, values=["начальное", "среднее", "высшее"], state='readonly')
        self.education.grid(column=0, row=6, padx=5, pady=(0, 5))
        
        # Метка тип ответов
        self.responseTypeLbl = Label(self, text="Ответы")
        self.responseTypeLbl.grid(column=0, row=7, padx=5, pady=(15, 5))
        
        # Поле для выбора типа ответов
        self.responseType = ttk.Combobox(self, values=["положительные", "отрицательные"], state='readonly')
        self.responseType.grid(column=0, row=8, padx=5, pady=(0, 5))
        
        # Кнопка Проанализировать
        self.analyzeBtn = ttk.Button(self, text="Проанализировать")
        self.analyzeBtn.grid(column=0, row=9, columnspan=3, ipady=10, ipadx=10, padx=2, pady=(15, 5))
    
    # Настроить строки и столбцы сетки
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
    
    # Отчистить поля ввода
    def clear(self):
        self.age.delete(0, END)