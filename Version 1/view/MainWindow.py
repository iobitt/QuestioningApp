# Импортируем графическуб библиотеку
from tkinter import *
# Импортируем базовое окно
from view.Window import Window
# Импортируем окно для отображения результатов опроса
from view.SurveyViewWindow import SurveyViewWindow
# Импортируем окно для манипуляции с вопросами анкеты
from view.QuestionnaireWindow import QuestionnaireWindow
# Импортируем окно для прохождения анкетирования
from view.PassSurveyWindow import PassSurveyWindow


# Основное окно
class MainWindow(Window):

    def __init__(self, parent, visible=False):
        super().__init__(parent, visible=visible)
        # Закрепляем окно на сетку
        self.grid(column=0, row=0, sticky=(N, S, E, W), pady=10, padx=10)
        # Индекс текущего активного дочернего окна
        self.activeWindowIndex = 0
        # Боковое меню
        self.sideBar = Listbox(self, width=20, font="Times 14")
        self.sideBar.grid(row=0, column=0, sticky=(N, S, E, W))
        # Добавляем разделы в список
        self.sideBar.insert(0, "Вопросы")
        self.sideBar.insert(1, "Анкетирование")
        self.sideBar.insert(2, "Статистика")
        # Устанавливаем окно по умолчанию
        self.sideBar.select_set(self.activeWindowIndex)
        
        # Окно для манипуляции вопросами анкеты
        self.questionnaireWindow = QuestionnaireWindow(self)
        self.questionnaireWindow.grid(row=0, column=1, sticky=(N, S, E, W))
        self.questionnaireWindow.setVisible(False)

        # Окно для отображения результатов опроса
        self.surveyViewWindow = SurveyViewWindow(self)
        self.surveyViewWindow.grid(row=0, column=1, sticky=(N, S, E, W))
        self.surveyViewWindow.setVisible(False)
        
        # Окно для прохождения опроса
        self.passSurveyWindow = PassSurveyWindow(self)
        self.passSurveyWindow.grid(row=0, column=1, sticky=(N, S, E, W))
        self.passSurveyWindow.setVisible(False)

    # Настройка столбцов и строк сетки
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=1)
