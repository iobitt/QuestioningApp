from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import messagebox
from model.Question import Question
from model.FileCabinet import FileCabinet
from model.Profile import Profile
from model.SinglyLinkedList import SinglyLinkedList
from model.Respondent import Respondent
import copy
from model.Profile import QuestionNotUpOrDownExc
from model.BinaryTreeSorting import BinaryTreeSorting


# Класс приложения
class Application(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.__exit)

        self.fileCabinet = self.load()

        self.createBtn = Button(self, text="Создать анкету", font=("Helvetica", 16), command=self.createProfile)

        handlers = {}
        handlers['fill'] = self.fill
        handlers['edit'] = self.edit
        handlers['analyse'] = self.analyse
        handlers['delete'] = self.delete
        self.profilesContainer = ProfilesListFrame(self, handlers)

        self.tuneGrid()
        self.setStyles()
        self._customizeWidgets()
        self._gridWidgets()

        self.profilesContainer.updateList(self.fileCabinet.getProfiles())

        # Настройка параметров главного меню
        self.__mainMenu = Menu(self)
        # Привязываем виджет меню к главному окну
        self.config(menu=self.__mainMenu)

        # Настройка подменю Файл
        # Создаём подменю
        self.__fileMenu = Menu(self.__mainMenu, tearoff=0)
        # Добавляем пункты меню и обработчики на нажатие на них кнопкой мыши
        self.__fileMenu.add_command(label="Сохранить", command=lambda: self.save())
        # Разделяет пункты подменю чертой
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Параметры", command=self.showConfigWindow)
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Выход", command=self.__exit)
        # Привязываем подменю к основному меню
        self.__mainMenu.add_cascade(label="Файл", menu=self.__fileMenu)

        # Настройка подменю, предоставляющее справочную информацию
        self.__helpMenu = Menu(self.__mainMenu, tearoff=0)
        # Добавляем пункты меню и обработчики на нажатие на них кнопкой мыши
        self.__helpMenu.add_command(label="Помощь")
        self.__helpMenu.add_command(label="О программе")
        # Привязываем подменю к основному меню
        self.__mainMenu.add_cascade(label="Справка", menu=self.__helpMenu)

    # Завершить программу
    def __exit(self):
        # Вызывает диалоговое окно с вопросом. Если пользователь отвечает да, то завершает программу
        if messagebox.askokcancel("Выйти?", "Вы уверены, что хотите выйти из программы?"):
            self.save()
            self.quit()
            self.destroy()

    # Настройка сетки
    def tuneGrid(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    # Настройка стилей
    def setStyles(self):
        bg = "#e3faff"
        self['bg'] = bg

        self.createBtn['bg'] = "#4da7db"
        self.createBtn['activebackground'] = "#4da7db"
        self.createBtn['fg'] = "white"
        self.createBtn['activeforeground'] = "white"
        self.createBtn['relief'] = FLAT

    # Настройка виджетов
    def _customizeWidgets(self):
        self.geometry("800x600+300+300")
        self.minsize(800, 600)
        self.title("Программа для проведения социального опроса населения")

    # Установка виджетов на сетку
    def _gridWidgets(self):
        self.createBtn.grid(column=0, row=0, sticky=(S, N, E, W), padx=(50, 50), pady=(50, 50), ipadx=30, ipady=10)
        self.profilesContainer.grid(column=0, row=1, columnspan=2, sticky=(S, N, E, W), padx=(50, 50), pady=(10, 50))

    # Запуск приложения
    def run(self):
        self.mainloop()

    def checkPermissions(self, permission):
        if self.fileCabinet.checkPermissions(permission):
            return True

        password = self.fileCabinet.getPassword()
        if password == "":
            return True

        window = PasswordInputWindow(self)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        passwordIn = window.getPassword()

        if passwordIn is None:
            return False

        if password != passwordIn:
            messagebox.showerror("Ошибка!", "Неверный пароль!")
            return False

        return True

    # Создать новый опрос
    def createProfile(self):
        if not self.checkPermissions("create"):
            return

        profile = Profile("Название опроса", "Описание опроса")
        window = ProfileEditWindow(self, profile)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        profile = window.getProfile()
        if profile:
            self.fileCabinet.addProfile(profile)
            profiles = self.fileCabinet.getProfiles()
            self.profilesContainer.updateList(profiles)

    # Пройти опрос
    def fill(self, event):
        if not self.checkPermissions("fill"):
            return

        window = ProfileFillWindow(self, event.widget.master.profile)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        answers = window.getAnswers()
        if answers:
            event.widget.master.profile.addRespondent(answers)

    # Изменить анкету
    def edit(self, event):
        if not self.checkPermissions("edit"):
            return

        respondentCount = event.widget.master.profile.getRespondentsCount()

        # if respondentCount != 0:
        #     messagebox.showerror("Ошибка!", "Нельзя изменять опрос после заполнения первой анкеты!")
        #     return

        copyProfile = copy.deepcopy(event.widget.master.profile)
        window = ProfileEditWindow(self, copyProfile)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        profile = window.getProfile()

        if profile:
            index = event.widget.master.profileIndex
            profiles = self.fileCabinet.getProfiles()

            profiles[index] = profile
            profiles = self.fileCabinet.getProfiles()
            self.profilesContainer.updateList(profiles)

    # Показать окно с анализом опроса
    def analyse(self, event):
        if not self.checkPermissions("analuse"):
            return

        window = AnalysisWindow(self, event.widget.master.profile.getAnalyseData(), event.widget.master.profile.getDataForGeneralTable2())
        window.grab_set()
        window.focus_set()
        window.wait_window()

    # Удалить опрос
    def delete(self, event):
        if not self.checkPermissions("delete"):
            return

        answer = messagebox.askyesno("Вы уверены?", "Удалить анкету?")
        if answer:
            self.fileCabinet.deleteProfile(event.widget.master.profileIndex)
            profiles = self.fileCabinet.getProfiles()
            self.profilesContainer.updateList(profiles)

    def load(self):
        try:
            data = FileCabinet.load("data/BD")
        except Exception as ex:
            data = FileCabinet()
        return data

    def save(self):
        FileCabinet.save("data/BD", self.fileCabinet)

    def showConfigWindow(self):
        password = self.fileCabinet.getPassword()
        if password != "":
            window = PasswordInputWindow(self)
            window.grab_set()
            window.focus_set()
            window.wait_window()
            passwordIn = window.getPassword()

            if passwordIn is None:
                return

            if password != passwordIn:
                messagebox.showerror("Ошибка!", "Неверный пароль!")
                return

        window = ConfigWindow(self)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        newPassword = window.getPassword()
        if newPassword is None:
            return
        access = window.getАccess()
        self.fileCabinet.setPassword(newPassword)
        self.fileCabinet.setAccess(access)


# Контнейнер для виджетов с полосой прокрутки
class ScrollFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        self.viewPort = Frame(self.canvas, background="#ffffff")

        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    # Перерисовка контейнера
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Перерисовка холста
    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    # Получить ссылку на контейнер
    def getFrame(self):
        return self.viewPort

    # Установить цвет фона
    def setBg(self, value):
        self.viewPort['bg'] = value

    # Получить элементы контейнера
    def getChildrens(self):
        return self.viewPort.winfo_children()


# Окно настройки прав доступа
class ConfigWindow(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.__password = None

        self.minsize(600, 400)
        self.maxsize(600, 400)
        bg = "#e3faff"
        self['bg'] = bg
        # Устанавливает заголовок окна
        self.title("Настройка прав доступа")
        self.tuneGrid()

        self.passwordLbl = Label(self, text="Пароль", font=("Helvetica", 20), anchor="w")
        self.passwordLbl['bg'] = bg
        self.passwordLbl.grid(column=0, row=0, sticky=(E, W), padx=30, pady=30)

        self.password = ttk.Entry(self, show="*", width=5, font=("Helvetica", 20))
        self.password.grid(column=1, row=0, columnspan=2, sticky=(E, W), padx=30, pady=30)

        self.fillLbl = Label(self, text="Заполнение", font=("Helvetica", 16), anchor="w")
        self.fillLbl['bg'] = bg
        self.fillLbl.grid(column=0, row=1, sticky=(E, W), padx=(30, 10))

        self.fill = IntVar()
        self.fill.set(0)
        all = Radiobutton(self, text="Все", variable=self.fill, value=0)
        all['bg'] = bg
        all.grid(column=1, row=1)
        admin = Radiobutton(self, text="Администратор", variable=self.fill, value=1)
        admin['bg'] = bg
        admin.grid(column=2, row=1)

        self.createLbl = Label(self, text="Создание", font=("Helvetica", 16), anchor="w")
        self.createLbl['bg'] = bg
        self.createLbl.grid(column=0, row=2, sticky=(E, W), padx=(30, 10))

        self.create = IntVar()
        self.create.set(0)
        all = Radiobutton(self, text="Все", variable=self.create, value=0)
        all['bg'] = bg
        all.grid(column=1, row=2)
        admin = Radiobutton(self, text="Администратор", variable=self.create, value=1)
        admin['bg'] = bg
        admin.grid(column=2, row=2)

        self.editLbl = Label(self, text="Изменение", font=("Helvetica", 16), anchor="w")
        self.editLbl['bg'] = bg
        self.editLbl.grid(column=0, row=3, sticky=(E, W), padx=(30, 10))

        self.edit = IntVar()
        self.edit.set(0)
        all = Radiobutton(self, text="Все", variable=self.edit, value=0)
        all['bg'] = bg
        all.grid(column=1, row=3)
        admin = Radiobutton(self, text="Администратор", variable=self.edit, value=1)
        admin['bg'] = bg
        admin.grid(column=2, row=3)

        self.analuseLbl = Label(self, text="Анализирование", font=("Helvetica", 16), anchor="w", justify="left")
        self.analuseLbl['bg'] = bg
        self.analuseLbl.grid(column=0, row=4, sticky=(E, W), padx=(30, 10))

        self.analuse = IntVar()
        self.analuse.set(0)
        all = Radiobutton(self, text="Все", variable=self.analuse, value=0)
        all['bg'] = bg
        all.grid(column=1, row=4)
        admin = Radiobutton(self, text="Администратор", variable=self.analuse, value=1)
        admin['bg'] = bg
        admin.grid(column=2, row=4)

        self.deleteLbl = Label(self, text="Удаление", font=("Helvetica", 16), anchor="w", justify="left")
        self.deleteLbl['bg'] = bg
        self.deleteLbl.grid(column=0, row=5, sticky=(E, W), padx=(30, 10))

        self.delete = IntVar()
        self.delete.set(0)
        all = Radiobutton(self, text="Все", variable=self.delete, value=0)
        all['bg'] = bg
        all.grid(column=1, row=5)
        admin = Radiobutton(self, text="Администратор", variable=self.delete, value=1)
        admin['bg'] = bg
        admin.grid(column=2, row=5)

        self.okBtn = Button(self, text="Сохранить", font=("Helvetica", 16), command=self.comlete)
        self.okBtn.grid(column=2, row=6, sticky=(E, W), padx=30, pady=(30, 10), ipadx=10, ipady=10)

        self.okBtn['bg'] = "#4da7db"
        self.okBtn['activebackground'] = "#4da7db"
        self.okBtn['fg'] = "white"
        self.okBtn['activeforeground'] = "white"
        self.okBtn['relief'] = FLAT

    def tuneGrid(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

    def comlete(self):
        self.__password = self.password.get()
        self.destroy()

    def getPassword(self):
        return self.__password

    def getАccess(self):
        access = set()

        if self.fill.get() == 0:
            access.add("fill")

        if self.create.get() == 0:
            access.add("create")

        if self.edit.get() == 0:
            access.add("edit")

        if self.analuse.get() == 0:
            access.add("analuse")

        if self.delete.get() == 0:
            access.add("delete")

        return access


# Окно ввода пароля
class PasswordInputWindow(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.__password = None

        self.minsize(600, 200)
        self.maxsize(600, 200)
        bg = "#e3faff"
        self['bg'] = bg
        # Устанавливает заголовок окна
        self.title("Ввод пароля")
        self.tuneGrid()

        self.passwordLbl = Label(self, text="Пароль", font=("Helvetica", 20), anchor="w")
        self.passwordLbl['bg'] = bg
        self.passwordLbl.grid(column=0, row=0, sticky=(E, W), padx=30, pady=30)

        self.password = ttk.Entry(self, show="*", width=5, font=("Helvetica", 20))
        self.password.grid(column=1, row=0, columnspan=2, sticky=(E, W), padx=30, pady=30)

        self.okBtn = Button(self, text="Ввести", font=("Helvetica", 16), command=self.comlete)
        self.okBtn.grid(column=2, row=1, sticky=(E, W), padx=30, pady=30, ipadx=10, ipady=10)

        self.okBtn['bg'] = "#4da7db"
        self.okBtn['activebackground'] = "#4da7db"
        self.okBtn['fg'] = "white"
        self.okBtn['activeforeground'] = "white"
        self.okBtn['relief'] = FLAT

    def tuneGrid(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

    def comlete(self):
        text = self.password.get()

        if len(text) == 0:
            messagebox.showerror("Ошибка!", "Пароль не может пустой!")
            return
        self.__password = text
        self.destroy()

    def getPassword(self):
        return self.__password


# Виджет для хранения списка анкет
class ProfilesListFrame(ScrollFrame):

    def __init__(self, parent, handlers):
        super().__init__(parent)

        self.handlers = handlers

        self.tuneGrid()

    # Настройка сетки
    def tuneGrid(self):
        self.columnconfigure(0, weight=0)

        self.rowconfigure(0, weight=0)

    # Обвновление списка
    def updateList(self, profiles):
        for child in self.getFrame().winfo_children():
            child.destroy()

        for index, profile in enumerate(profiles):
            item = ProfilesListItem(self.getFrame(), profile, index, self.handlers)
            item.pack(side=TOP, fill=BOTH, expand=1, padx=10, pady=10)


# Элемент списка анкет
class ProfilesListItem(Frame):

    def __init__(self, parent, profile, profileIndex, handlers):
        super().__init__(parent)
        self.tuneGrid()

        self.profileIndex = profileIndex
        self.profile = profile

        self.name = Label(self, text=profile.getName(), font=("Helvetica", 16), anchor="w")
        self.name.grid(column=0, row=0, sticky=(S, N, E, W), padx=20, pady=10)

        self.fill = Button(self, text="Пройти")
        self.fill.bind('<Button-1>', handlers['fill'])
        self.fill.grid(column=1, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=10)

        self.edit = Button(self, text="Изменить")
        self.edit.bind('<Button-1>', handlers['edit'])
        self.edit.grid(column=2, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=10)

        self.analysis = Button(self, text="Анализ")
        self.analysis.bind('<Button-1>', handlers['analyse'])
        self.analysis.grid(column=3, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=10)

        self.delete = Button(self, text="Удалить")
        self.delete.bind('<Button-1>', handlers['delete'])
        self.delete.grid(column=4, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=10)

        self.setStyle()

    # Задать стили элементов
    def setStyle(self):
        self.fill['bg'] = "#4da7db"
        self.fill['activebackground'] = "#4da7db"
        self.fill['fg'] = "white"
        self.fill['activeforeground'] = "white"
        self.fill['relief'] = FLAT

        self.edit['bg'] = "#4da7db"
        self.edit['activebackground'] = "#4da7db"
        self.edit['fg'] = "white"
        self.edit['activeforeground'] = "white"
        self.edit['relief'] = FLAT

        self.analysis['bg'] = "#4da7db"
        self.analysis['activebackground'] = "#4da7db"
        self.analysis['fg'] = "white"
        self.analysis['activeforeground'] = "white"
        self.analysis['relief'] = FLAT

        self.delete['bg'] = "#4da7db"
        self.delete['activebackground'] = "#4da7db"
        self.delete['fg'] = "white"
        self.delete['activeforeground'] = "white"
        self.delete['relief'] = FLAT

    # Настроить сетку
    def tuneGrid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=0)

        self.rowconfigure(0, weight=0)


""" Окно для создания и редактирования анкеты """


# Окно редактирования анкеты
class ProfileEditWindow(Toplevel):

    def __init__(self, parent, profile):
        super().__init__(parent)

        # Устанавливает размеры окна приложения 800 на 600 точек и сдвигает окно на 300 точек по вертикали и горизонтали
        self.geometry("800x600+300+300")
        self.minsize(800, 600)
        bg = "#e3faff"
        self['bg'] = bg
        # Устанавливает заголовок окна
        self.title("Редактирование анкеты")
        self.tuneGrid()

        self.greetingBtn = Button(self, text="Окно приветствия", font=("Helvetica", 16))
        self.greetingBtn.grid(column=0, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=30, ipady=10)
        self.greetingBtn.bind('<Button-1>', self.changeTab)

        self.questionBtn = Button(self, text="Окно вопросов", font=("Helvetica", 16))
        self.questionBtn.grid(column=1, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=30, ipady=10)
        self.questionBtn.bind('<Button-1>', self.changeTab)

        self.completeBtn = Button(self, text="Сохранить", font=("Helvetica", 16))
        self.completeBtn.grid(column=2, row=0, sticky=(S, N, E, W), padx=10, pady=10, ipadx=30, ipady=10)
        self.completeBtn.bind('<Button-1>', self.complete)

        self.greetingFrame = GreetingFrameEdit(self, profile)

        self.mainFrame = QuestionsEditFrame(self, profile)

        self.profile = profile
        self.newProfile = None

        self.setStyle()

    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def setStyle(self):
        bg = "#e3faff"
        self['bg'] = bg

        self.greetingBtn['bg'] = "#4da7db"
        self.greetingBtn['activebackground'] = "#4da7db"
        self.greetingBtn['fg'] = "white"
        self.greetingBtn['activeforeground'] = "white"
        self.greetingBtn['relief'] = FLAT

        self.questionBtn['bg'] = "#4da7db"
        self.questionBtn['activebackground'] = "#4da7db"
        self.questionBtn['fg'] = "white"
        self.questionBtn['activeforeground'] = "white"
        self.questionBtn['relief'] = FLAT

        self.completeBtn['bg'] = "#4da7db"
        self.completeBtn['activebackground'] = "#4da7db"
        self.completeBtn['fg'] = "white"
        self.completeBtn['activeforeground'] = "white"
        self.completeBtn['relief'] = FLAT

    def complete(self, event):
        name = self.greetingFrame.getName()

        if len(name) == 0:
            messagebox.showerror("Ошибка!", "Название анкеты не задано!")
            return

        description = self.greetingFrame.getDescription()
        questions = self.mainFrame.getQuestions()

        if len(questions) == 0:
            messagebox.showerror("Ошибка!", "В анкете нет ни одного вопроса!")
            return

        profile = Profile(name, description)
        for question in questions:
            profile.addQuestion(question)

        for respondent in self.profile.getRespondents():
            profile.addRespondent(respondent)

        self.newProfile = profile
        self.destroy()

    def getProfile(self):
        return self.newProfile

    def changeTab(self, event):
        if event.widget is self.greetingBtn:
            self.greetingFrame.grid(column=0, row=1, columnspan=3, sticky=(S, N, E, W))
            self.mainFrame.grid_remove()
        elif event.widget is self.questionBtn:
            self.mainFrame.grid(column=0, row=1, columnspan=3, sticky=(S, N, E, W))
            self.greetingFrame.grid_remove()


# Редактирование вкладки приветствия
class GreetingFrameEdit(Frame):

    def __init__(self, parent, profile):
        super().__init__(parent)
        bg = "#e3faff"
        self['bg'] = bg

        self.nameLbl = Label(self, text="Название", font=("Helvetica", 26), anchor="w")
        self.nameLbl['bg'] = bg

        # Название анкеты
        self.name = Entry(self, font=("Helvetica", 26))

        self.descriptionLbl = Label(self, text="Описание", font=("Helvetica", 26), anchor="w")
        self.descriptionLbl['bg'] = bg

        # Описание
        self.description = Text(self, font=("Helvetica", 16))

        self.tuneGrid()
        self.gridAll()

        self.name.insert(0, profile.getName())
        self.description.insert(1.0, profile.getDescription())

    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)

    def gridAll(self):
        self.nameLbl.grid(column=0, row=0, sticky=(S, N, E, W), pady=(50, 30), padx=30)
        self.name.grid(column=0, row=1, sticky=(S, N, E, W), pady=(0, 40), padx=30)
        self.descriptionLbl.grid(column=0, row=2, sticky=(S, N, E, W), pady=(50, 30), padx=30)
        self.description.grid(column=0, row=3, sticky=(S, N, E, W), pady=(0, 30), padx=30)

    def getName(self):
        return self.name.get()

    def getDescription(self):
        return self.description.get(1.0, END)


# Вкладка редактирования вопросов
class QuestionsEditFrame(ScrollFrame):

    def __init__(self, parent, profile):
        super().__init__(parent)

        self.profile = profile
        container = self.canvas

        self.menu = Menu(tearoff=0)
        self.menu.add_command(label="Добавить вопрос с одиночным выбором", command=self.addSingleChoiceQuestion)
        self.menu.add_command(label="Добавить вопрос с множественным выбором", command=self.addMultipleChoiceQuestion)
        self.menu.add_command(label="Добавить текстовый вопрос", command=self.addTextQuestion)
        container.bind("<Button-3>", self.showContextMenu)

        self.updateView()

    def showContextMenu(self, event):
        self.menu.post(event.x_root, event.y_root)

    # Обновить представление
    def updateView(self):
        # Удалить старые элементы
        for child in self.getFrame().winfo_children():
            child.destroy()

        self.addQuestions()

    def addQuestions(self):
        for index, question in enumerate(self.profile.getQuestions()):
            if question.getType() == 1:
                q = TextQuestionView(self.getFrame(), question, index)
                q.pack(side=TOP, fill=BOTH, expand=1)
            elif question.getType() == 2:
                q = SingleChoiceQuestionView(self.getFrame(), question, index)
                q.pack(side=TOP, fill=BOTH, expand=1)
            elif question.getType() == 3:
                q = MultipleChoiceQuestionView(self.getFrame(), question, index)
                q.pack(side=TOP, fill=BOTH, expand=1)

            qMenu = Menu(tearoff=0)
            qMenu.add_command(label="Добавить вопрос с одиночным выбором", command=self.addSingleChoiceQuestion)
            qMenu.add_command(label="Добавить вопрос с множественным выбором", command=self.addMultipleChoiceQuestion)
            qMenu.add_command(label="Добавить текстовый вопрос", command=self.addTextQuestion)
            qMenu.add_command(label="Поднять вопрос в списке")
            qMenu.add_command(label="Опустить вопрос в списке")
            # qMenu.add_command(label="Изменить вопрос")
            qMenu.add_command(label="Удалить вопрос")

            def showMenu(event):
                qMenu.entryconfig("Поднять вопрос в списке", command=lambda: self.questionUp(event.widget.index))
                qMenu.entryconfig("Опустить вопрос в списке", command=lambda: self.questionDown(event.widget.index))
                # qMenu.entryconfig("Изменить вопрос", command=lambda: self.editQuestion(event.widget.question))
                qMenu.entryconfig("Удалить вопрос", command=lambda: self.deleteQuestion(event.widget.index))
                qMenu.post(event.x_root, event.y_root)

            q.bind("<Button-3>", showMenu)

    def addTextQuestion(self):
        if self.profile.getRespondentsCount() != 0:
            messagebox.showwarning("Предупреждение!", "Нельзя создавать вопросы после начала анкетирования!")
            return

        question = Question("Название вопроса", "", 1, 1)
        window = TextQuestionEdit(self, question)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        question = window.getQuestion()
        if question:
            self.profile.addQuestion(question)
            self.updateView()

    def addSingleChoiceQuestion(self):
        if self.profile.getRespondentsCount() != 0:
            messagebox.showwarning("Предупреждение!", "Нельзя создавать вопросы после начала анкетирования!")
            return

        question = Question("Вопрос 1", "", 2, 1)
        window = SingleQuestionEdit(self, question)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        question = window.getQuestion()
        if question:
            self.profile.addQuestion(question)
            self.updateView()

    def addMultipleChoiceQuestion(self):
        if self.profile.getRespondentsCount() != 0:
            messagebox.showwarning("Предупреждение!", "Нельзя создавать вопросы после начала анкетирования!")
            return

        question = Question("Название вопроса", "", 3, 1)
        window = MultipleQuestionEdit(self, question)
        window.grab_set()
        window.focus_set()
        window.wait_window()
        question = window.getQuestion()
        if question:
            self.profile.addQuestion(question)
            self.updateView()

    def getQuestions(self):
        questions = []
        for item in self.getFrame().winfo_children():
            questions.append(item.getQuestion())
        return questions

    # Изменить вопрос
    def editQuestion(self, question):
        print("Реализуй меня!")

    # Удалить вопрос
    def deleteQuestion(self, index):
        self.profile.deleteQuestion(index)
        self.updateView()

    # Поднять вопрос
    def questionUp(self, index):
        try:
            self.profile.questionUp(index)
            self.updateView()
        except QuestionNotUpOrDownExc:
            messagebox.showinfo("Примечание", "Вопрос и так стоит на верхней позиции!")

    # Опустить вопрос
    def questionDown(self, index):
        try:
            self.profile.questionDown(index)
            self.updateView()
        except QuestionNotUpOrDownExc:
            messagebox.showinfo("Примечание", "Вопрос и так стоит на нижней позиции!")


# Основа для редактирования вопроса
class QuestionBasisEdit(Toplevel):

    def __init__(self, parent, question):
        super().__init__(parent)
        self.minsize(800, 400)

        if type(question) is not Question:
            raise TypeError("question must be Question!")

        self.question = question
        self.newQuestion = None

        self.headingLbl = Label(self, text="Заголовок", font=("Helvetica", 24), anchor="w")

        # Заголовок вопроса
        self.heading = Entry(self, text="Вопрос", font=("Helvetica", 24))

        self.hintLbl = Label(self, text="Подсказка", font=("Helvetica", 24), anchor="w")

        # Подзаголовок вопроса
        self.hint = Entry(self, text="Подсказка", font=("Helvetica", 15))

        self.saveBtn = Button(self, text="Сохранить", font=("Helvetica", 16), command=self.save)

        self.pin()
        self.tuneGrid()

        self.setStyles()

    def setStyles(self):
        bg = "#e3faff"
        self['bg'] = bg
        self.headingLbl['bg'] = bg
        self.hintLbl['bg'] = bg

        self.saveBtn['bg'] = "#4da7db"
        self.saveBtn['activebackground'] = "#4da7db"
        self.saveBtn['fg'] = "white"
        self.saveBtn['activeforeground'] = "white"
        self.saveBtn['relief'] = FLAT

    # Настройка столбцов и строк сетки
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=0)

    def pin(self):
        self.headingLbl.grid(row=0, column=0, columnspan=3, sticky="nswe", pady=(20, 10), padx=20)
        self.heading.grid(row=1, column=0, columnspan=3, sticky="nswe", pady=(10, 10), padx=20)
        self.hintLbl.grid(row=2, column=0, columnspan=3, sticky="nswe", pady=(20, 10), padx=20)
        self.hint.grid(row=3, column=0, columnspan=3, sticky="nswe", pady=(10, 10), padx=20)
        self.saveBtn.grid(row=5, column=2, sticky="we", pady=(10, 20), padx=20, ipadx=10, ipady=10)

    def getQuestion(self):
        return self.newQuestion

    def save(self):
        raise VirtualMethodCallEx("Нельзя вызвать абстрактный метод!")

    def setHeading(self, value):
        self.heading.delete(0, END)
        self.heading.insert(0, value)

    def setHint(self, value):
        self.hint.delete(0, END)
        self.hint.insert(0, value)

    def getHeading(self):
        return self.heading.get()

    def getHint(self):
        return self.hint.get()

    def fill(self):
        raise VirtualMethodCallEx("Нельзя вызвать абстрактный метод!")


# Виджет для редактирования текстового вопроса
class TextQuestionEdit(QuestionBasisEdit):

    def __init__(self, parent, question):
        super().__init__(parent, question)

        if self.question.getType() != 1:
            raise ValueError("Неверный тип вопроса!")

        self.fill()

    def save(self):
        if len(self.getHeading()) == 0:
            messagebox.showerror("Ошибка!", "Введите название вопроса!")
            return

        self.newQuestion = Question(self.getHeading(), self.getHint(), 1, 1)

        self.destroy()

    def fill(self):
        self.setHeading(self.question.getHeading())
        self.setHint(self.question.getHint())


# Виджет для редактирования вопроса с выбором
class ChoiceQuestionEdit(QuestionBasisEdit):

    def __init__(self, parent, question):
        super().__init__(parent, question)

        self.optionContainer = ScrollFrame(self)
        self.optionContainer.grid(column=0, row=4, columnspan=3, sticky=(E, W, N, S), pady=(10, 10), padx=30)

        self.addBtn = Button(self, text="Добавить ответ", font=("Helvetica", 16), command=self.addOption)
        self.addBtn.grid(row=5, column=0, sticky="we", pady=(30, 50), padx=30, ipadx=10, ipady=10)

        self.addBtn['bg'] = "#4da7db"
        self.addBtn['activebackground'] = "#4da7db"
        self.addBtn['fg'] = "white"
        self.addBtn['activeforeground'] = "white"
        self.addBtn['relief'] = FLAT

        self.fill()

    def addOption(self, value=""):
        option = ttk.Entry(self.optionContainer.getFrame(), font=("Helvetica", 14))
        option.insert(0, value)
        option.pack(side=TOP, fill=X, pady=(10, 10), padx=10)

    def fill(self):
        self.setHeading(self.question.getHeading())
        self.setHint(self.question.getHint())

        for option in self.question.getOptions():
            self.addOption(option)


# Виджет для редактирования вопроса с одиночным выбором
class SingleQuestionEdit(ChoiceQuestionEdit):

    def __init__(self, parent, question):
        super().__init__(parent, question)

        if self.question.getType() != 2:
            raise ValueError("Неверный тип вопроса!")

    def save(self):
        if len(self.getHeading()) == 0:
            messagebox.showerror("Ошибка!", "Введите название вопроса!")
            return

        question = Question(self.getHeading(), self.getHint(), 2, 1)

        for option in self.optionContainer.getFrame().winfo_children():
            option = option.get()
            if len(option):
                question.addOption(option)

        if len(question.getOptions()) < 2:
            messagebox.showerror("Ошибка!", "Добавьте не менее двух ответов!")
            return

        self.newQuestion = question
        self.destroy()


# Виджет для редактирования вопроса с множественным выбором
class MultipleQuestionEdit(ChoiceQuestionEdit):

    def __init__(self, parent, question):
        super().__init__(parent, question)

        if self.question.getType() != 3:
            raise ValueError("Неверный тип вопроса!")

    def save(self):
        if len(self.getHeading()) == 0:
            messagebox.showerror("Ошибка!", "Введите название вопроса!")
            return

        question = Question(self.getHeading(), self.getHint(), 3, 1)

        for option in self.optionContainer.getFrame().winfo_children():
            option = option.get()
            if len(option):
                question.addOption(option)

        if len(question.getOptions()) < 2:
            messagebox.showerror("Ошибка!", "Добавьте не менее двух ответов!")
            return

        self.newQuestion = question
        self.destroy()


# # Окно редактирования текстового вопроса
# class TextQuestionEditWindow(Toplevel):
#
#     def __init__(self, parent, question):
#         super().__init__(parent)
#
#         # Заголовок вопроса
#         self.heading = Entry(self)
#         # Подзаголовок вопроса
#         self.hint = Entry(self)
#         # Ответ пользователя
#         self.answer = Text(self)
#         # Кнопка сохранить
#         self.saveBtn = Button(self, text="Сохранить")
#
#         self.tuneGrid()
#         self._widgetsConfigure()
#         self._gridWidgets()
#
#     def tuneGrid(self):
#         self.columnconfigure(0, weight=9)
#         self.columnconfigure(1, weight=1)
#
#         self.rowconfigure(0, weight=0)
#         self.rowconfigure(1, weight=0)
#         self.rowconfigure(2, weight=1)
#         self.rowconfigure(3, weight=0)
#
#     def _widgetsConfigure(self):
#         self.heading.configure(font=("Helvetica", 16))
#         self.setHeading("Напишите свой вопрос здесь...")
#
#         self.hint.configure(font=("Helvetica", 16))
#         self.setHint("Дополнительное описание...")
#
#         self.answer.configure(width=25, height=5, wrap=WORD, state='disabled')
#         self.answer.insert(1.0, "Поля для ввода ответа")
#
#     def _gridWidgets(self):
#         self.heading.grid(column=0, row=0, columnspan=2, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))
#         self.hint.grid(column=0, row=1, columnspan=2, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))
#         self.answer.grid(column=0, row=2, columnspan=2, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))
#         self.saveBtn.grid(column=1, row=3, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10), ipadx=10, ipady=10)
#
#     def _unGridAll(self):
#         childs = self.winfo_children()
#         for child in childs:
#             child.grid_remove()
#
#     # Установить заголовок
#     def setHeading(self, heading):
#         self.heading.delete(0, END)
#         self.heading.insert(0, heading)
#
#     # Получить заголовок
#     def getHeading(self):
#         return self.heading.get()
#
#     # Установить подзаголовок
#     def setHint(self, hint):
#         self.hint.delete(0, END)
#         self.hint.insert(0, hint)
#
#     # Получить подзаголовок
#     def getHint(self):
#         return self.hint.get()


""" Представление вопросов """


# Основа для представления вопроса
class QuestionBasisView(Frame):

    def __init__(self, parent, question, index):
        super().__init__(parent)

        self.question = question
        self.index = index

        # Заголовок вопроса
        self.heading = Label(self, text=question.getHeading(), font=("Helvetica", 24))
        # Подзаголовок вопроса
        self.hint = Label(self, text=question.getHint(), font=("Helvetica", 15))

        self.pin()
        self.tuneGrid()
        self.setStyle()

    # Настройка столбцов и строк сетки
    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

    def pin(self):
        self.heading.grid(sticky="w", pady=(10, 10), padx=10)
        self.hint.grid(sticky="w", pady=(0, 15), padx=10)

    def getAnswers(self):
        raise VirtualMethodCallEx("Нельзя вызвать абстрактный метод!")

    def getQuestion(self):
        raise VirtualMethodCallEx("Нельзя вызвать абстрактный метод!")

    def getHeading(self):
        return self.heading['text']

    def getHint(self):
        return self.hint['text']

    def setStyle(self):
        bg = "#e3faff"
        self['bg'] = bg
        self.heading['bg'] = bg
        self.hint['bg'] = bg


# Виджет представления текстового вопроса
class TextQuestionView(QuestionBasisView):

    def __init__(self, parent, question, index):
        super().__init__(parent, question, index)

        self.entry = ttk.Entry(self, font=('Helvetica', 14))
        self.entry.grid(column=0, row=2, sticky=(E, W), padx=(10, 30), pady=(0, 50))

    def getAnswers(self):
        answers = []

        text = self.entry.get()
        if text:
            answers.append(text)

        return answers

    def getQuestion(self):
        question = Question(self.getHeading(), self.getHint(), 1, 1)
        return question


# Виджет представления вопроса с выбором ответов
class ChoiceQuestionView(QuestionBasisView):

    def __init__(self, parent, question, index):
        super().__init__(parent, question, index)
        self.tuneGrid()

        self.optionContainer = Frame(self, bg="#e3faff")
        self.optionContainer.grid(column=0, row=2, sticky=(S, N, E, W), pady=(0, 50))
        self.rowconfigure(2, weight=1)

        self.addOptions()

    def addOptions(self):
        for option in self.question.getOptions():
            btn = Button(self.optionContainer, text=option, font=("Helvetica", 14))

            btn['bg'] = "#4da7db"
            btn['activebackground'] = "#4da7db"
            btn['fg'] = "white"
            btn['activeforeground'] = "white"
            btn['relief'] = FLAT

            btn.bind('<Button-1>', self.chooseAnswer)
            btn.pack(side=TOP, fill=BOTH, expand=1, padx=30, pady=10, ipadx=10, ipady=10)

    def chooseAnswer(self, event):
        raise VirtualMethodCallEx("Нельзя вызвать абстрактный метод!")

    def getAnswers(self):
        answers = SinglyLinkedList()

        for btn in self.optionContainer.winfo_children():
            if btn['bg'] == "blue":
                answers.append(btn['text'])
        return answers


# Виджет представления вопроса с одиночным выбором
class SingleChoiceQuestionView(ChoiceQuestionView):

    def __init__(self, parent, question, index):
        super().__init__(parent, question, index)

    def chooseAnswer(self, event):
        if event.widget['bg'] == "blue":
            self.clearButtonsColor()
            event.widget['bg'] = "#4da7db"
        else:
            self.clearButtonsColor()
            event.widget['bg'] = "blue"

    def clearButtonsColor(self):
        for btn in self.optionContainer.winfo_children():
            btn['bg'] = "#4da7db"

    def getQuestion(self):
        question = Question(self.getHeading(), self.getHint(), 2, 1)

        for item in self.optionContainer.winfo_children():
            question.addOption(item['text'])

        return question


# Виджет представления вопроса с множественным выбором
class MultipleChoiceQuestionView(ChoiceQuestionView):

    def __init__(self, parent, question, index):
        super().__init__(parent, question, index)

    def chooseAnswer(self, event):
        if event.widget['bg'] == "blue":
            event.widget['bg'] = "#4da7db"
        else:
            event.widget['bg'] = "blue"

    def getQuestion(self):
        question = Question(self.getHeading(), self.getHint(), 3, 1)

        for item in self.optionContainer.winfo_children():
            question.addOption(item['text'])

        return question


""" Анализ результатов """


# Окно анализа результатов анкеты
class AnalysisWindow(Toplevel):

    def __init__(self, parent, profile, dataForGenetalTable):
        super().__init__(parent)
        self.minsize(800, 600)

        self.title = Label(self, text=profile['name'], font=("Helvetica", 26))
        self.title.grid(column=1, row=0, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))

        self.container = ScrollFrame(self)
        self.container.grid(column=1, row=2, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))

        self.generalResultsTable = GeneralResultsTable(self.container.getFrame(), dataForGenetalTable)
        # self.generalResultsTable.grid(column=1, row=1, sticky=(S, N, E, W), padx=(10, 10), pady=(10, 10))
        self.generalResultsTable.pack(side=TOP, fill=X, expand=1, padx=(50, 50), pady=(20, 50))

        self.tuneGrid()
        self.setStyle()
        self.addQuestions(profile['questions'])

    def tuneGrid(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=3)

        self.rowconfigure(0, weight=0)
        # self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

    def setStyle(self):
        bg = "#e3faff"
        self['bg'] = bg

        self.title['bg'] = bg

    def addQuestions(self, questions):
        for question in questions:
            name = Label(self.container.getFrame(), text=question['heading'], font=("Helvetica", 16), anchor="w")
            name['bg'] = "white"
            name.pack(side=TOP, fill=BOTH, expand=1, padx=(30, 30), pady=(20, 0))

            if question['type'] == 1:
                self.addTextQuestion(question)
            elif question['type'] == 2:
                self.addSingleChoiceQuestion(question)
            elif question['type'] == 3:
                self.addMultipleChoiceQuestion(question)

    def addTextQuestion(self, question):
        listbox = Listbox(self.container.getFrame(), font=("Helvetica", 16))
        listbox['highlightbackground'] = "black"

        for value in question["values"]:
            listbox.insert(END, value)

        listbox.pack(side=TOP, fill=BOTH, expand=1, padx=(30, 30), pady=(20, 100))

    def addSingleChoiceQuestion(self, question):
        labels = [i+1 for i in range(len(question['values'][0]))]
        fig, ax = plt.subplots()
        ax.pie(question['values'][1], labels=labels, autopct='%1.1f%%')

        chart = Chart(fig, self.container.getFrame())
        chartTk = chart.get_tk_widget()
        chartTk.pack(side=TOP, fill=BOTH, expand=1, padx=(10, 10), pady=(0, 0))

        tree = AnalysisTable(self.container.getFrame())
        tree['bg'] = "white"
        tree.pack(side=TOP, fill=BOTH, expand=1, padx=(10, 10), pady=(0, 100))

        for i in range(len(question['values'][0])):
            tree.insert("", END, text=str(i + 1),
                        values=(str(question['values'][0][i]), str(question['values'][1][i]), "{0:.1f}%".format(question['values'][2][i])))

    def addMultipleChoiceQuestion(self, question):
        x = np.arange(len(question['values'][0]))

        fig, ax = plt.subplots()
        plt.bar(x, question['values'][2])
        plt.xticks(x, (i+1 for i in range(len(question['values'][0]))))
        plt.yticks(np.arange(0, 101, step=10))

        chart = Chart(fig, self.container.getFrame())
        chartTk = chart.get_tk_widget()
        chartTk.pack(side=TOP, fill=BOTH, expand=1, padx=(10, 10), pady=(0, 0))

        tree = AnalysisTable(self.container.getFrame())
        tree['bg'] = "white"
        tree.pack(side=TOP, fill=BOTH, expand=1, padx=(10, 10), pady=(0, 100))

        for i in range(len(question['values'][0])):
            tree.insert("", END, text=str(i + 1),
                        values=(str(question['values'][0][i]), str(question['values'][1][i]), "{0:.1f}%".format(question['values'][2][i])))


# Общая таблица результатов анкетирования
class GeneralResultsTable(Frame):

    def __init__(self, parent, data):
        super().__init__(parent)
        self['bg'] = "white"

        self.data = data

        self.title = Label(self, text="Общая таблица результатов анкетирования", font=("Helvetica", 16), anchor="w")
        self.title['bg'] = "white"
        self.title.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W), pady=10, padx=10)

        self.table = ttk.Treeview(self)
        self.table.grid(column=0, row=1, columnspan=2, sticky=(N, S, E, W), pady=10, padx=10)

        # Прокрутка таблицы по оси x
        self.xScrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.table.xview)
        self.xScrollbar.grid(column=0, row=2, columnspan=2, sticky=(E, W))
        self.table.configure(xscrollcommand=self.xScrollbar.set)

        # Прокрутка таблицы по оси y
        self.yScrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.yScrollbar.grid(column=2, row=1, sticky=(N, S))
        self.table.configure(yscrollcommand=self.yScrollbar.set)

        self.sortByNameBtn = Button(self, text="Отсортировать по названию", font=("Helvetica", 14), command=self.sortByName)
        self.sortByNameBtn.grid(column=0, row=3, sticky=(N, S, E, W), pady=10, padx=10, ipady=10)
        self.sortByNameBtn['bg'] = "#4da7db"
        self.sortByNameBtn['activebackground'] = "#4da7db"
        self.sortByNameBtn['fg'] = "white"
        self.sortByNameBtn['activeforeground'] = "white"
        self.sortByNameBtn['relief'] = FLAT

        self.sortByTypeBtn = Button(self, text="Отсортировать по типу", font=("Helvetica", 14), command=self.sortByType)
        self.sortByTypeBtn.grid(column=1, row=3, sticky=(N, S, E, W), pady=10, padx=10, ipady=10)
        self.sortByTypeBtn['bg'] = "#4da7db"
        self.sortByTypeBtn['activebackground'] = "#4da7db"
        self.sortByTypeBtn['fg'] = "white"
        self.sortByTypeBtn['activeforeground'] = "white"
        self.sortByTypeBtn['relief'] = FLAT

        self.tuneGrid()
        self.updateView()

    def tuneGrid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)

    def updateView(self):
        # Отчищаю таблицу
        for i in self.table.get_children():
            self.table.delete(i)

        self.table["columns"] = ([str(i+1) for i in range(len(self.data['headings']))])
        self.table.heading("#0", text="№", anchor=W)
        for index in range(len(self.data["headings"])):
            self.table.heading(str(index+1), text=self.data["headings"][index], anchor=W)

        for index in range(len(self.data["body"])):
            self.table.insert("", index, text=str(index + 1), values=(self.data["body"][index]))

    def updateView2(self):
        self.table["columns"] = ([str(i+1) for i in range(len(self.data))])
        self.table.heading("#0", text="№", anchor=W)
        for index in range(len(self.data)):
            self.table.heading(str(index+1), text=self.data[index][0], anchor=W)

        for index in range(1, len(self.data[0])):
            self.table.insert("", index, text=str(index), values=([self.data[i][index] for i in range(len(self.data))]))

    def sortByName(self):
        BinaryTreeSorting.sort(self.data["body"], key=lambda value: value[0])
        self.updateView()

    def sortByType(self):
        BinaryTreeSorting.sort(self.data["body"], key=lambda value: value[1])
        self.updateView()


# Таблица с со статистикой ответов
class AnalysisTable(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self)
        self.tree.pack()
        self.tree["columns"] = ("1", "2", "3")
        self.tree.heading("#0", text="№", anchor=W)
        self.tree.heading("1", text="Вариант ответа", anchor=W)
        self.tree.heading("2", text="Ответы", anchor=W)
        self.tree.heading("3", text="Доля", anchor=W)

    def insert(self, parent, index, text="", values=tuple()):
        self.tree.insert(parent, index, text=text, values=values)


# График
class Chart(FigureCanvasTkAgg):

    def __init__(self, fig, root):
        super().__init__(fig, master=root)
        self.draw()


""" Окно для прохождения опроса """


# Окно для прохождения опроса
class ProfileFillWindow(Toplevel):

    def __init__(self, parent, profile):
        super().__init__(parent)

        # Устанавливает размеры окна приложения 800 на 600 точек и сдвигает окно на 300 точек по вертикали и горизонтали
        self.geometry("800x600+300+300")
        self.minsize(800, 600)
        # Устанавливает заголовок окна
        self.title("Заполнение анкеты")
        self.tuneGrid()

        self.greetingFrame = GreetingFrame(self, profile, self.start)
        self.greetingFrame.start = self.start
        self.greetingFrame.grid(column=0, row=0, sticky=(S, N, E, W))

        self.mainFrame = MainFrame(self, profile.getQuestions(), self.back, self.complete)

        self.answers = None

    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=1)

        # Настройка строк
        self.rowconfigure(0, weight=1)

    def start(self):
        self.greetingFrame.grid_remove()
        self.mainFrame.grid(column=0, row=0, sticky=(S, N, E, W))

    def back(self):
        self.mainFrame.grid_remove()
        self.greetingFrame.grid(column=0, row=0, sticky=(S, N, E, W))

    def complete(self):
        respondent = Respondent("", 1, 1, 1)
        questions = self.mainFrame.getQuestions()
        for i in questions:
            answer = i.getAnswers()
            if len(answer) == 0:
                messagebox.showerror("Ошибка!", "Сначала нужно ответить на все вопросы!")
                return
            respondent.addAnswer(answer)
        self.answers = respondent
        messagebox.showinfo("Успешно!", "Анкета успешно добавлена!")
        self.destroy()

    def getAnswers(self):
        return self.answers


# Вкладка приветствия
class GreetingFrame(Frame):

    def __init__(self, parent, profile, start):
        super().__init__(parent)

        # Название анкеты
        self.name = Label(self, text=profile.getName(), font=("Helvetica", 26))

        # Описание
        self.description = Label(self, text=profile.getDescription(), font=("Helvetica", 16))

        # Кнопка Начать опрос
        self.startBtn = Button(self, text="Начать опрос сейчас", font=("Helvetica", 16), command=start)

        self.tuneGrid()
        self.gridAll()
        self.setStyles()

    def setStyles(self):
        # bg = "#dcf4fa"
        bg = "#e3faff"
        self['bg'] = bg
        self.name['bg'] = bg
        self.description['bg'] = bg
        self.startBtn['bg'] = "#4da7db"
        self.startBtn['activebackground'] = "#4da7db"
        self.startBtn['fg'] = "white"
        self.startBtn['activeforeground'] = "white"
        self.startBtn['relief'] = FLAT

    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=30)
        self.columnconfigure(1, weight=40)
        self.columnconfigure(2, weight=30)

        # Настройка строк
        self.rowconfigure(0, weight=45)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=45)

    def gridAll(self):
        self.name.grid(column=1, row=1, sticky=(S, N, E, W), pady=(0, 40))
        self.description.grid(column=1, row=2, sticky=(S, N, E, W), pady=(0, 30))
        self.startBtn.grid(column=1, row=3, ipadx=50, ipady=10)


# Вкладка с вопросами
class MainFrame(Frame):

    def __init__(self, parent, questions, back, complete):
        super().__init__(parent)

        self.questionContainer = ScrollFrame(self)
        self.questionContainer.grid(column=1, row=0, rowspan=3, sticky=(S, N, E, W))

        self.backBtn = Button(self, text="Назад", font=("Helvetica", 14), command=back)
        self.backBtn.grid(column=0, row=1, ipadx=20, ipady=10)

        self.completeBtn = Button(self, text="Завершить", font=("Helvetica", 14), command=complete)
        self.completeBtn.grid(column=2, row=1, ipadx=20, ipady=10)

        self.tuneGrid()
        self.setStyles()
        self.addQuestions(questions)

    def tuneGrid(self):
        # Настройка колонок
        self.columnconfigure(0, weight=20)
        self.columnconfigure(1, weight=60)
        self.columnconfigure(2, weight=20)

        # Настройка строк
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

    def addQuestions(self, questions):
        for question in questions:
            if question.getType() == 1:
                q = TextQuestionView(self.questionContainer.getFrame(), question, -1)
                q.pack(side=TOP, fill=BOTH, expand=1)
            elif question.getType() == 2:
                q = SingleChoiceQuestionView(self.questionContainer.getFrame(), question, -1)
                q.pack(side=TOP, fill=BOTH, expand=1)
            elif question.getType() == 3:
                q = MultipleChoiceQuestionView(self.questionContainer.getFrame(), question, -1)
                q.pack(side=TOP, fill=BOTH, expand=1)

    def getQuestions(self):
        return self.questionContainer.getChildrens()

    def setStyles(self):
        bg = "#e3faff"
        self['bg'] = bg

        self.questionContainer.setBg(bg)

        self.backBtn['bg'] = "#4da7db"
        self.backBtn['activebackground'] = "#4da7db"
        self.backBtn['fg'] = "white"
        self.backBtn['activeforeground'] = "white"
        self.backBtn['relief'] = FLAT

        self.completeBtn['bg'] = "#4da7db"
        self.completeBtn['activebackground'] = "#4da7db"
        self.completeBtn['fg'] = "white"
        self.completeBtn['activeforeground'] = "white"
        self.completeBtn['relief'] = FLAT


# Исключение "Вызов виртуального метода"
class VirtualMethodCallEx(Exception):
    def __init__(self, text):
        self.txt = text
