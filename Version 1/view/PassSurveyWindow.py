from tkinter import *
from tkinter import ttk
from view.Window import Window


# Окно для прохождения анкетирования
class PassSurveyWindow(Window):

    def __init__(self, parent, visible=False):
        super().__init__(parent, visible=visible)

        # Дочернее окно для начала анкетирования
        self.startFrame = Frame(self)
        # Вызываем функцию для настройки его строк и столбцов
        self.startFrameTuneGrid()
        self.startFrame.grid(column=0, row=0, sticky=(S, N, E, W))

        # Стиль для внешнего вида кнопок
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 20))

        # Кнопка Начать анкетирование
        self.startBtn = ttk.Button(self.startFrame, text="Начать", style="my.TButton")
        self.startBtn.grid(column=1, row=1, sticky=(S, N, E, W))

        # Дочернее окно для прохождения анкетирования
        self.surveyFrame = Frame(self)
        self.surveyFrame.grid(column=0, row=0, sticky=(S, N, E, W), padx=20, pady=10)
        # Вызываем функцию для настройки его строк и столбцов
        self.surveyFrameTuneGrid()
        # По умолчанию скрываем окно
        self.surveyFrame.grid_remove()

        # Метка Первая частт вопросов
        self.part1 = Label(self.surveyFrame, text="Часть 1", font="Times 20")
        self.part1.grid(column=0, row=0, sticky="w", pady=(0, 10))

        # Метка Поле ввода возраста
        self.ageLbl = Label(self.surveyFrame, text="Возраст")
        self.ageLbl.grid(column=0, row=1, sticky="w")

        # Поле ввода возраста
        self.age = Entry(self.surveyFrame, width=5)
        self.age.grid(column=1, row=1, sticky=(E, W))

        # Метка Ввод пола
        self.genderLbl = Label(self.surveyFrame, text="Пол")
        self.genderLbl.grid(column=0, row=2, sticky="w")

        # Переменная для хранения значения пола
        self.gender = IntVar()
        # Радио-кнопка Мужской пол
        self.man = Radiobutton(self.surveyFrame, text="Мужской", value=1, variable=self.gender)
        self.man.grid(column=1, row=2, sticky="w")
        # Радио-кнопка Женский пол
        self.woman = Radiobutton(self.surveyFrame, text="Женский", value=2, variable=self.gender)
        self.woman.grid(column=2, row=2, sticky="w")

        # Метка уровень образования
        self.educationLbl = Label(self.surveyFrame, text="Уровень образования")
        self.educationLbl.grid(column=0, row=3, sticky="w")

        # Переменная для хранения значения пола
        self.education = IntVar()
        # Радио-кнопка Начальное образование
        self.early = Radiobutton(self.surveyFrame, text="Начальный", value=1, variable=self.education)
        self.early.grid(column=1, row=3, sticky="w")
        # Радио-кнопка Среднее образование
        self.secondary = Radiobutton(self.surveyFrame, text="Средний", value=2, variable=self.education)
        self.secondary.grid(column=2, row=3, sticky="w")
        # Радио-кнопка Высшее образование
        self.high = Radiobutton(self.surveyFrame, text="Высший", value=3, variable=self.education)
        self.high.grid(column=3, row=3, sticky="w")

        # Метка Часть 2
        self.part2 = Label(self.surveyFrame, text="Часть 2", font="Times 20")
        self.part2.grid(column=0, row=4, sticky="w", pady=(20, 10))

        # Виджет для отображения вопросов
        self.qText = Text(self.surveyFrame)
        self.qText.grid(column=0, row=5, columnspan=9, sticky=(S, N, E, W))

        # Кнопка для положительного ответа на вопрос
        self.yesBtn = ttk.Button(self.surveyFrame, text="Да")
        self.yesBtn.grid(column=2, row=6, sticky=(S, N, E, W), padx=10, pady=10)

        # Кнопка для отрицательного ответа на вопрос
        self.noBtn = ttk.Button(self.surveyFrame, text="Нет")
        self.noBtn.grid(column=4, row=6, sticky=(S, N, E, W), padx=10, pady=10)

        # Кнопка для завершения анкетирования
        self.completeBtn = ttk.Button(self.surveyFrame, text="Завершить")
        self.completeBtn.grid(column=8, row=8, sticky=(S, N, E, W), padx=10)
        
        # Кнопка для отмены анкетирования
        self.cancelBtn = ttk.Button(self.surveyFrame, text="Отменить")
        self.cancelBtn.grid(column=0, row=8, sticky=(S, N, E, W), padx=10)
    
    # Настройка строк и столбцов окна
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=1)
    
    # Настройка строк и столбцов окна начала анкетирования
    def startFrameTuneGrid(self):
        # Настройка колонок
        self.startFrame.columnconfigure(0, weight=40)
        self.startFrame.columnconfigure(1, weight=20)
        self.startFrame.columnconfigure(2, weight=40)

        # Настройка строк
        self.startFrame.rowconfigure(0, weight=45)
        self.startFrame.rowconfigure(1, weight=10)
        self.startFrame.rowconfigure(2, weight=45)

    # Настройка строк и столбцов окна ответы на вопросы
    def surveyFrameTuneGrid(self):
        # Настройка колонок
        self.surveyFrame.columnconfigure(0, weight=10)
        self.surveyFrame.columnconfigure(1, weight=10)
        self.surveyFrame.columnconfigure(2, weight=10)
        self.surveyFrame.columnconfigure(3, weight=10)
        self.surveyFrame.columnconfigure(4, weight=10)
        self.surveyFrame.columnconfigure(5, weight=10)
        self.surveyFrame.columnconfigure(6, weight=10)
        self.surveyFrame.columnconfigure(7, weight=10)
        self.surveyFrame.columnconfigure(8, weight=10)

        # Настройка строк
        self.surveyFrame.rowconfigure(5, weight=70)
        self.surveyFrame.rowconfigure(6, weight=5)
        self.surveyFrame.rowconfigure(7, weight=25)
        self.surveyFrame.rowconfigure(8, weight=10)
    
    # Отчистить поля ввода
    def clear(self):
        self.age.delete(0, END)
        self.qText.delete(1.0, END)
