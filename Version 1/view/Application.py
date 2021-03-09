# Импортируем графическую библиотеку tkinter
from tkinter import *
# Из модуля tkinter импортируем модуль для создания файловых диалогов с пользователем
from tkinter import filedialog
# Из модуля tkinter импортируем модуль для создания информационных или критических сообщений
from tkinter import messagebox
# Импортируем класс главного окна
from view.MainWindow import MainWindow
# Импортируем класс, предназначенный для проведения опросов
from model.Survey import Survey
# Импортируем класс Ответный лист
from model.ResponseSheet import ResponseSheet
# Импортируем класс Односвязный список
from model.SinglyLinkedList import SinglyLinkedList
# Импортируем модуль, в котором реализована сортировка бинарным деревом
from model.BinaryTreeSorting import BinaryTreeSorting


# Главный класс программы. Наследуется от класса Tk - класс, представляющий окно верхнего уровня приложения
class Application(Tk):

    # Конструктор класса. Принимает путь к файлу-сохранению
    def __init__(self, fileName=None):
        # Вызывает конструктор базового класса
        Tk.__init__(self)
        # Устанавливает размеры окна приложения 800 на 600 точек и сдвигает окно на 300 точек по вертикали и горизонтали
        self.geometry("800x600+300+300")
        # Устанавливает заголовок окна
        self.title("Опросник")
        # Указывает окну растягивать дочерние элементы по вертикали и горизонтали
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Устанавливает действие на нажатие кнопки закрытия главного окна приложения
        self.protocol("WM_DELETE_WINDOW", self.__exit)


        # Настройка параметров главного меню
        self.__mainMenu = Menu(self)
        # Привязываем виджет меню к главному окну
        self.config(menu=self.__mainMenu)

        # Настройка подменю Файл
        # Создаём подменю
        self.__fileMenu = Menu(self.__mainMenu, tearoff=0)
        # Добавляем пункты меню и обработчики на нажатие на них кнопкой мыши
        self.__fileMenu.add_command(label="Создать опрос", command=self.__createSurvey)
        self.__fileMenu.add_command(label="Открыть опрос", command=self.__openFileWithDialog)
        self.__fileMenu.add_command(label="Закрыть опрос", state="disabled", command=self.__closeSurvey)
        # Разделяет пункты подменю чертой
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Сохранить", state="disabled", command=self.__saveFile)
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


        # Создаём главное окно приложения
        self.__mainWindow = MainWindow(self)
        # По умолчанию делаем его невидимым
        self.__mainWindow.setVisible(False)


        # Ссылка на текущий проект. Если None, то нет открытого проекта
        self.__survey = None
        # Ссылка на ответный лист(заполняемую анкету). None, если в текущий момент анкетирование не проводится
        self.__responseSheet = None
        # Путь к текущему файлу проекта
        self.fileName = None


        # Добаление событий к элементам
        # Добавляем событие к боковому меню: функция будет вызываться при выделении элемента списка
        self.__mainWindow.sideBar.bind('<<ListboxSelect>>', self.__onSelectSideBarItem)
        # Вызываем эту функцию, чтобы применить настройки по умолчанию
        self.__onSelectSideBarItem(None)

        # Добавляет обработчики к окну редактирования вопросов
        self.__mainWindow.questionnaireWindow.addBtn['command'] = self.__addQuestion
        self.__mainWindow.questionnaireWindow.changeBtn['command'] = self.__changeQuestion
        self.__mainWindow.questionnaireWindow.deleteBtn['command'] = self.__deleteQuestion
        self.__mainWindow.questionnaireWindow.upBtn['command'] = self.__upQuestion
        self.__mainWindow.questionnaireWindow.downBtn['command'] = self.__downQuestion

        # Добавляет обработчики к окну для прохождения анкетирования
        self.__mainWindow.passSurveyWindow.startBtn['command'] = self.__startSurvey
        self.__mainWindow.passSurveyWindow.yesBtn['command'] = self.__yesAnswerToQuestion
        self.__mainWindow.passSurveyWindow.noBtn['command'] = self.__noAnswerToQuestion
        self.__mainWindow.passSurveyWindow.completeBtn['command'] = self.__addResponseSheet
        self.__mainWindow.passSurveyWindow.cancelBtn['command'] = self.__cancelSurvey

        # Добавляет обработчики к окну вывода результатов анкетирования
        self.__mainWindow.surveyViewWindow.analysisWindow.analyzeBtn['command'] = self.__analyze
        self.__mainWindow.surveyViewWindow.sortBtn['command'] = self.__sort

        # Если входной параметр fileName не равен None, то сохраняем путь к проекту и открываем его
        if fileName:
            self.fileName = fileName
            self.__openFile()

    # Завершить программу
    def __exit(self):
        # Вызывает диалоговое окно с вопросом. Если пользователь отвечает да, то завершает программу
        if messagebox.askokcancel("Выйти?", "Вы уверены, что хотите выйти из программы?"):
            self.destroy()

    # Создать новый проект - новый чистый опрос без вопросов и ответов
    def __createSurvey(self):
        # Если в текущий момент запущен другой проект
        if self.__survey:
            # Пытаемся его закрыть. Если пользователь отказался закрывать открытый проект, то выходим из функции
            if self.__closeSurvey() is False:
                return
            # Рекурсивно вызываем эту же функцию, чтобы создать новый проект. К этому моменту функция closeSurvey() уже закрыла открытый ранее проект
            self.__createSurvey()
        else:
            # Делаем видимым главное окно
            self.__mainWindow.setVisible(True)
            # Разблокрируем кнопки главного меню, которые раньше были не доступны для нажатия
            self.__fileMenu.entryconfigure(2, state="normal")
            self.__fileMenu.entryconfigure(4, state="normal")
            # Создаём новый опрос
            self.__survey = Survey()
            # Обвновляем таблицу с результатами опроса: она могла сохранить данные прошлого опроса
            self.__updateSurveyTable()

    # Загрузить сохранённый ранее проект
    def __openFile(self):
        try:
            # Загружаем сохраннёный ранее опрос из файла
            self.__survey = Survey.loadFromFile(self.fileName)
            # Делаем видимым главное окно
            self.__mainWindow.setVisible(True)
            # Разблокируем кнопки меню
            self.__fileMenu.entryconfigure(2, state="normal")
            self.__fileMenu.entryconfigure(4, state="normal")
            # Обновляем боковое меню
            self.__onSelectSideBarItem(None)
            # Обновляем список вопросов
            self.__updateQuestionListBox()
        except Exception:
            messagebox.showerror("Ошибка!", "Не удалось загрузить проект!")

    # Открыть диалоговое окно для выбора файла, после чего загрузить проект
    def __openFileWithDialog(self):
        # Если открыт другой проект, пытаемся его сначала закрыть. Если пользователь отказался его закрывать, завершаем функцию
        if self.__closeSurvey() is False:
            return
        # Получаем путь к расположению файла проекта
        self.fileName = filedialog.askopenfilename(filetypes=(("Survey files", "*.surv"), ("All files", "*.*")))
        # Если путь не корректный, то завершаем функцию
        if self.fileName == "":
            self.fileName = None
            return
        # Открываем проект
        self.__openFile()

    # Сохранить проект в файл
    def __saveFile(self):
        # Если файл был открыт ранее, то сохраняем обратно в этот же файл
        if self.fileName:
            # Сохраняем проект
            self.__survey.saveToFile(self.fileName)
            messagebox.showinfo("Успешно!", "Опрос сохранён!")
        else:
            # Запрашиваем у пользователя расположение для сохранения файла
            self.fileName = filedialog.asksaveasfilename(filetypes=(("Survey files", "*.surv"), ("All files", "*.*")))
            # Если путь не выбран, завершаем функцию
            if self.fileName == "":
                self.fileName = None
                return
            # Сохраняем файл
            self.__survey.saveToFile(self.fileName + ".surv")
            messagebox.showinfo("Успешно!", "Опрос сохранён!")

    # Закрыть текущий проект
    def __closeSurvey(self):
        # Если открытого проекта нет, то завершаем функцию
        if self.__survey is None:
            return True

        # Создаём диалоговое окно. Если пользователь подтверждает закрытие проекта
        if messagebox.askokcancel("Закрыть?", "Вы уверены, что хотите закрыть текущий опрос? Не сохранённые изменения будут утеряны..."):
            # Скрываем главное окно
            self.__mainWindow.setVisible(False)
            # Удаляем ссылку на старый объект опроса
            self.__survey = None
            # Удаляем ссылку на старый объект ответного листа
            self.__responseSheet = None
            # Делаем не активными некоторые кнопки меню
            self.__fileMenu.entryconfigure(2, state="disabled")
            self.__fileMenu.entryconfigure(4, state="disabled")
            # Приводим окна в виду по умолчанию (отчищаем все введенные поля и другое)
            self.__mainWindow.passSurveyWindow.clear()
            self.__mainWindow.questionnaireWindow.clear()
            self.__mainWindow.passSurveyWindow.startFrame.grid()
            self.__mainWindow.passSurveyWindow.surveyFrame.grid_remove()
            self.fileName = None
            # Возвращаем True, если пользователь согласился закрыть текущий проект
            return True
        else:
            # В противном случае False
            return False

    # Функция выполняется при выборе элемента бокового меню
    def __onSelectSideBarItem(self, el):
        # Получаем индекс выбранного элемента списка
        index = self.__mainWindow.sideBar.curselection()
        # Если ни одна строка не выбрана, завершаем функцию
        if len(index) == 0:
            return
        # Выбираем первый элемент кортежа
        index = index[0]
        # Скрываем все дочерние окна главного меню
        self.__mainWindow.questionnaireWindow.setVisible(False)
        self.__mainWindow.passSurveyWindow.setVisible(False)
        self.__mainWindow.surveyViewWindow.setVisible(False)
        # Записываем индекс в переменную класса
        self.__mainWindow.activeWindowIndex = index
        # Делаем видимым выбранное окно
        if self.__mainWindow.activeWindowIndex == 0:
            self.__mainWindow.questionnaireWindow.setVisible(True)
        elif self.__mainWindow.activeWindowIndex == 1:
            self.__mainWindow.passSurveyWindow.setVisible(True)
        elif self.__mainWindow.activeWindowIndex == 2:
            self.__mainWindow.surveyViewWindow.setVisible(True)
            self.__updateSurveyTable()

    # Обновить таблицу вывода результатов опроса
    def __updateSurveyTable(self):
        # Отчищаю таблицу
        for i in self.__mainWindow.surveyViewWindow.tree.get_children():
            self.__mainWindow.surveyViewWindow.tree.delete(i)
        # Добаляем таблице заголовки
        self.__mainWindow.surveyViewWindow.tree.heading("#0", text="Вопросы", anchor=W)
        self.__mainWindow.surveyViewWindow.tree["columns"] = tuple(range(1, self.__survey.getResponseSheetCount() + 1))
        for i in self.__mainWindow.surveyViewWindow.tree["columns"]:
            self.__mainWindow.surveyViewWindow.tree.heading(i, text="Респондент №{0}".format(i), anchor=W)

        # Получаю список возрастов респондентов
        age = SinglyLinkedList()
        for i in range(self.__survey.getResponseSheetCount()):
            # Получаем ответный лист
            responseSheet = self.__survey.getResponseSheet(i)
            # Из него берём возраст респондента и записываем его в список
            age.append(responseSheet.getAge())

        # Получаю список полов респондентов
        gender = SinglyLinkedList()
        for i in range(self.__survey.getResponseSheetCount()):
            responseSheet = self.__survey.getResponseSheet(i)
            gender1 = responseSheet.getGender()
            if gender1 == 1:
                gender.append("муж.")
            else:
                gender.append("жен.")

        # Получаю список уровней образования
        education = SinglyLinkedList()
        for i in range(self.__survey.getResponseSheetCount()):
            responseSheet = self.__survey.getResponseSheet(i)
            education1 = responseSheet.getEducation()
            if education1 == 1:
                education.append("нач.")
            elif education1 == 2:
                education.append("сред.")
            else:
                education.append("высш.")

        # Заполняю первые три строки таблицы: возраст, пол, образование респондента
        self.__mainWindow.surveyViewWindow.tree.insert("", END, text="Возраст", values=tuple(age))
        self.__mainWindow.surveyViewWindow.tree.insert("", END, text="Пол", values=tuple(gender))
        self.__mainWindow.surveyViewWindow.tree.insert("", END, text="Образование", values=tuple(education))

        # Добавляю ответы на вопросы типа да/нет
        for i in range(self.__survey.getQuestionCount()):
            # Вопрос
            question = self.__survey.getQuestion(i)
            # Ответы респондентов на данный вопрос
            response = SinglyLinkedList()
            # Прохожу по списку ответов респондентов и выбираю ответы на вопрос с индексом i
            for j in range(self.__survey.getResponseSheetCount()):
                responseSheet = self.__survey.getResponseSheet(j)
                response1 = responseSheet.getAnswer(i)
                if response1:
                    response.append("Да")
                else:
                    response.append("Нет")
            # Добавляю строку: вопрос и ответы на него
            self.__mainWindow.surveyViewWindow.tree.insert("", END, text=question, values=tuple(response))

    # Добавить вопрос в анкету
    def __addQuestion(self):
        if self.__responseSheet is not None:
            messagebox.showerror("Ошибка", "Нельзя изменять вопросы во время прохождения анкетирования!")
            return

        try:
            # Получаем вопрос, введёный пользователем в текстовое поле
            text = self.__mainWindow.questionnaireWindow.entry.get()
            # Добавляем вопрос в анкету
            self.__survey.addQuestion(text)
            # Обновляем список вопросов на экране пользователя
            self.__updateQuestionListBox()
            # Удаляем вопрос из поля ввода
            self.__mainWindow.questionnaireWindow.entry.delete(0, END)
        # Если вопрос не удалось добавить в анкету, выводим причину
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))
            return

    # Изменить вопрос анкеты
    def __changeQuestion(self):
        if self.__responseSheet is not None:
            messagebox.showerror("Ошибка", "Нельзя изменять вопросы во время прохождения анкетирования!")
            return

        try:
            # Получаем текст из поля ввода
            text = self.__mainWindow.questionnaireWindow.entry.get()
            # Получаем кортеж с номерами выделенных строк
            index = self.__mainWindow.questionnaireWindow.listBox.curselection()
            # Если ни одна строка не выбрана, завершаем функцию
            if len(index) == 0:
                return
            # Выбираем первый элемент кортежа
            index = index[0]
            # Изменяем вопрос с выбранным индексом
            self.__survey.changeQuestion(text, index)
            # Обновляем список вопросов на экране пользователя
            self.__updateQuestionListBox()
            # Отчищаем поле ввода
            self.__mainWindow.questionnaireWindow.entry.delete(0, END)
            # Устанавливаем фокус на элемент списка с идексом index
            self.__mainWindow.questionnaireWindow.listBox.select_set(index)
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))
            return

    # Удалить вопрос из анкеты
    def __deleteQuestion(self):
        if self.__responseSheet is not None:
            messagebox.showerror("Ошибка", "Нельзя изменять вопросы во время прохождения анкетирования!")
            return

        try:
            # Получаем кортеж с номерами выделенных строк
            index = self.__mainWindow.questionnaireWindow.listBox.curselection()
            # Если ни одна строка не выбрана, завершаем функцию
            if len(index) == 0:
                return
            # Выбираем первый элемент кортежа
            index = index[0]
            # Удаляем вопрос с данным индексом из анкеты
            self.__survey.deleteQuestion(index)
            # Обновляем список вопросов на экране пользователя
            self.__updateQuestionListBox()
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))
            return

    # Поднять вопрос в списке вопросов
    def __upQuestion(self):
        if self.__responseSheet is not None:
            messagebox.showerror("Ошибка", "Нельзя изменять вопросы во время прохождения анкетирования!")
            return

        # Получаем кортеж с номерами выделенных строк
        index = self.__mainWindow.questionnaireWindow.listBox.curselection()
        # Если ни одна строка не выбрана, завершаем функцию
        if len(index) == 0:
            return
        # Выбираем первый элемент кортежа
        index = index[0]

        try:
            # Поднимаем вопрос в списке
            self.__survey.upQuestion(index)
            # Обновляем список вопросов на экране пользователя
            self.__updateQuestionListBox()
            # Устанавливаем фокус на элементе списка
            self.__mainWindow.questionnaireWindow.listBox.select_set(index - 1)
        except Exception as ex:
            if ex.__str__() == "Вопрос и так стоит на самой верхней позиции!":
                pass
            else:
                messagebox.showerror("Ошибка", str(ex))
                return

    # Опустить вопрос в списке
    def __downQuestion(self):
        if self.__responseSheet is not None:
            messagebox.showerror("Ошибка", "Нельзя изменять вопросы во время прохождения анкетирования!")
            return

        # Получаем кортеж с номерами выделенных строк
        index = self.__mainWindow.questionnaireWindow.listBox.curselection()
        # Если ни одна строка не выбрана, завершаем функцию
        if len(index) == 0:
            return
        # Выбираем первый элемент кортежа
        index = index[0]

        try:
            # Опускаем вопрос в списке
            self.__survey.downQuestion(index)
            # Обновляем список вопросов на экране пользователя
            self.__updateQuestionListBox()
            # Устанавливаем фокус на элементе списка
            self.__mainWindow.questionnaireWindow.listBox.select_set(index + 1)
        except Exception as ex:
            if ex.__str__() == "Вопрос и так стоит на самой нижней позиции!":
                pass
            else:
                messagebox.showerror("Ошибка", str(ex))
                return

    # Обновить список вопросов на экране пользователя
    def __updateQuestionListBox(self):
        # Отчащаем список
        count = self.__mainWindow.questionnaireWindow.listBox.size()
        self.__mainWindow.questionnaireWindow.listBox.delete(0, count - 1)
        # Заполняем список
        for i in range(self.__survey.getQuestionCount()):
            self.__mainWindow.questionnaireWindow.listBox.insert(i, self.__survey.getQuestion(i))

    # Начать анкетирование
    def __startSurvey(self):
        try:
            # Создаём ответный лист с заданным количеством вопросов
            self.__responseSheet = ResponseSheet(self.__survey.getQuestionCount())
            # Скрываем окно Начать анкетирование
            self.__mainWindow.passSurveyWindow.startFrame.grid_remove()
            # Показываем окно прохождения анкетирования
            self.__mainWindow.passSurveyWindow.surveyFrame.grid()
            # Отчищаем окно Прохождения анкетирования
            self.__mainWindow.passSurveyWindow.clear()
            # Показываем первый вопрос
            self.__nextQuestion()
            # Делаем активными кнопки Да и нет
            self.__mainWindow.passSurveyWindow.yesBtn['state'] = "normal"
            self.__mainWindow.passSurveyWindow.noBtn['state'] = "normal"
        except TypeError:
            messagebox.showerror("Ошибка", "Не возможно начать анкетирование! Не добавлен ни один вопрос!")
            return

    # Отменить анкетирование
    def __cancelSurvey(self):
        # Удаляем ссылку на созданный ранее Ответный лист
        self.__responseSheet = None
        # Показываем окно Начать анкетирование
        self.__mainWindow.passSurveyWindow.startFrame.grid()
        # Скрваем окно анкетирования
        self.__mainWindow.passSurveyWindow.surveyFrame.grid_remove()
        # Отчищаем окно прохождения анкетирования
        self.__mainWindow.passSurveyWindow.clear()

    # Ответить положительно на вопрос
    def __yesAnswerToQuestion(self):
        # Добавляем положительный ответ в Ответный лист
        self.__responseSheet.addAnswer(True)
        # Меняем вопрос
        self.__nextQuestion()

    # Ответить отрицательно на вопрос
    def __noAnswerToQuestion(self):
        # Добавляем отрицательный ответ
        self.__responseSheet.addAnswer(False)
        # Меняем вопрос
        self.__nextQuestion()

    # Устанавливаем следующий вопрос
    def __nextQuestion(self):
        # Получаем количество вопросов, на которые дан ответ
        count = self.__responseSheet.getCount()
        # Получаем количество вопросов, на которые нужно дать ответ
        maxCount = self.__responseSheet.getMaxCount()
        # Если есть не отвеченные вопросы
        if count + 1 <= maxCount:
            # Удаляем старый вопрос
            self.__mainWindow.passSurveyWindow.qText.delete(1.0, END)
            # Устанавливаем новый вопрос
            self.__mainWindow.passSurveyWindow.qText.insert(1.0, self.__survey.getQuestion(count))
        # Если на все вопросы даны ответы
        else:
            # Удаляем старый вопрос
            self.__mainWindow.passSurveyWindow.qText.delete(1.0, END)
            # Выводим сообщение, что на все вопросы даны ответы
            self.__mainWindow.passSurveyWindow.qText.insert(1.0, "На все вопросы были даны ответы!")
            # Деактивируем кнопки Да и Нет
            self.__mainWindow.passSurveyWindow.yesBtn['state'] = "disabled"
            self.__mainWindow.passSurveyWindow.noBtn['state'] = "disabled"

    # Добавить ответный лист в опрос
    def __addResponseSheet(self):
        # Добавляем возраст в ответный лист
        try:
            # Получаем возраст из поля
            age = int(self.__mainWindow.passSurveyWindow.age.get())
            # Добавляем его в ответный лист
            self.__responseSheet.setAge(age)
        except ValueError:
            messagebox.showerror("Ошибка", "Не корректно введён возраст!")
            return
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))
            return

        # Добавляем пол в ответный лист
        gender = self.__mainWindow.passSurveyWindow.gender.get()
        if gender == 0:
            messagebox.showerror("Ошибка!", "Пол не выбран!")
            return
        self.__responseSheet.setGender(gender)

        # Добавляем образование в ответный лист
        education = self.__mainWindow.passSurveyWindow.education.get()
        if education == 0:
            messagebox.showerror("Ошибка!", "Уровень образования не выбран!")
            return
        self.__responseSheet.setEducation(education)

        # Добавляем ответный лист в опрос
        try:
            self.__survey.addResponseSheet(self.__responseSheet)
        except TypeError:
            messagebox.showerror("Ошибка!", "Вы не ответили на все вопросы типа да/нет!")
            return

        messagebox.showinfo("Успешно!", "Ответ успешно добавлен!")
        # Готовим программу для нового анкетирования
        self.__mainWindow.passSurveyWindow.startFrame.grid()
        self.__mainWindow.passSurveyWindow.surveyFrame.grid_remove()
        self.__responseSheet = None

    # Посчитать количество ответов, удовлетворяющих условиям
    def __analyze(self):
        # Получаем выделенную строку таблицы
        focus = self.__mainWindow.surveyViewWindow.tree.focus()
        # Определяем вопрос, по которому нужно провести подсчёт
        question = self.__mainWindow.surveyViewWindow.tree.index(focus) - 3
        if question < 0:
            messagebox.showinfo("Ошибка!", "Вопрос не выбран!")
            return

        # Параметр, который указывает, считать ответы большие age или наборот меньшие age
        ageInequality = self.__mainWindow.surveyViewWindow.analysisWindow.ageInequality.get()
        if ageInequality == 'больше':
            ageInequality = 1
        elif ageInequality == 'меньше':
            ageInequality = 2
        else:
            messagebox.showerror("Ошибка!", "Не верно указано неравенство поля Возраст!")
            return

        # Получаем возраст
        age = int(self.__mainWindow.surveyViewWindow.analysisWindow.age.get())

        # Получаем пол респондента
        gender = self.__mainWindow.surveyViewWindow.analysisWindow.gender.get()
        if gender == 'мужской':
            gender = 1
        elif gender == 'женский':
            gender = 2
        else:
            messagebox.showerror("Ошибка!", "Не корректное значение поля Пол!")
            return

        # Получаем поле образование
        education = self.__mainWindow.surveyViewWindow.analysisWindow.education.get()
        if education == 'начальное':
            education = 1
        elif education == 'среднее':
            education = 2
        elif education == 'высшее':
            education = 3
        else:
            messagebox.showerror("Ошибка!", "Не корректное значение поля Образование!")
            return

        # Получаем параметр, какие ответы нужно считать: положительные или отрицательные
        responseType = self.__mainWindow.surveyViewWindow.analysisWindow.responseType.get()
        if responseType == 'положительные':
            responseType = True
        elif responseType == 'отрицательные':
            responseType = False
        else:
            messagebox.showerror("Ошибка!", "Не корректное значение поля Ответы!")
            return
        try:
            # Считаем и выводим результат
            result = self.__survey.countByParameters(question, age, ageInequality, gender, education, responseType)
            messagebox.showinfo("Результаты!", "Результатов, удовлетворяющих заданным условиям: {0}".format(result))
        except Exception as ex:
            messagebox.showerror("Ошибка!", str(ex))

    # Сортирует таблицу с результатами опроса по выделенной строке
    def __sort(self):
        # Получаем выделенную строку
        focus = self.__mainWindow.surveyViewWindow.tree.focus()
        # Получаем её номер
        lineNumber = self.__mainWindow.surveyViewWindow.tree.index(focus)
        # Получаем список Ответных листов
        responseSheets = self.__survey.getResponseSheets()
        # Если их меньше 2х, то сортировать нет смысла
        if len(responseSheets) < 2:
            return
        # Если первая строка, то сортируем по возрасту
        if lineNumber == 0:
            BinaryTreeSorting.sort(responseSheets, key=lambda val: val.getAge())
        # Если вторая строка, то сортируем по полу
        elif lineNumber == 1:
            BinaryTreeSorting.sort(responseSheets, key=lambda val: val.getGender())
        # Если третья строка, то сортируем по образованию
        elif lineNumber == 2:
            BinaryTreeSorting.sort(responseSheets, key=lambda val: val.getEducation())
        # Если линия имеет индекс больше 2, то сортируем по вопросу типа да/нет
        elif lineNumber > 2:
            BinaryTreeSorting.sort(responseSheets, key=lambda val: val.getAnswer(lineNumber - 3))
        # Обновляем таблицу с результатами ответов
        self.__updateSurveyTable()
