# Импортируем Односвязный список
from model.SinglyLinkedList import SinglyLinkedList
# Импортируем Ответный лист
from model.ResponseSheet import ResponseSheet
# Импортируем класс Вопросник
from model.Questionnaire import Questionnaire


# Класс Опрос
class Survey:

    def __init__(self):
        # Вопросник
        self.__questionnaire = Questionnaire()
        # Ответные листы
        self.__responseSheets = SinglyLinkedList()

    # Добавить вопрос
    def addQuestion(self, question):
        if len(self.__responseSheets) != 0:
            raise Exception("Добавлять вопросы после начала анкетирования нельзя!")

        self.__questionnaire.addQuestion(question)

    # Добавить ответный лист
    def addResponseSheet(self, responseSheet):
        # Проверка: переменная responseSheet должна быть типа ResponseSheet. Иначе выбрасывается исключение
        if type(responseSheet) is not ResponseSheet:
            raise TypeError("Входной параметр должен быть типа ResponseSheet!")

        if responseSheet.getCount() != self.__questionnaire.getCount():
            raise TypeError("Количество ответов не совпадает с количеством вопросов в вопроснике!")

        # Проверяем, все ли ответы записаны. Если не все, функция выкинет исключение
        responseSheet.isAllReplyReceived()

        # Если не было брошено исключений, то добавляем элемент в список
        self.__responseSheets.append(responseSheet)

    # Возвращает количество вопросов в вопроснике
    def getQuestionCount(self):
        return self.__questionnaire.getCount()

    # Возвращает вопрос по индексу
    def getQuestion(self, index):
        return self.__questionnaire.getQuestion(index)

    # Изменяет вопрос
    def changeQuestion(self, question, index):
        if len(self.__responseSheets) != 0:
            raise Exception("Изменять вопросы после начала анкетирования нельзя!")

        self.__questionnaire.changeQuestion(question, index)

    # Удаляет вопрос из вопросника
    def deleteQuestion(self, index):
        if len(self.__responseSheets) != 0:
            raise Exception("Изменять вопросы после начала анкетирования нельзя!")

        self.__questionnaire.deleteQuestion(index)

    # Поднять вопрос в списке вопросов
    def upQuestion(self, index):
        if len(self.__responseSheets) != 0:
            raise Exception("Изменять вопросы после начала анкетирования нельзя!")

        self.__questionnaire.up(index)

    # Опустить вопрос в списке вопросов
    def downQuestion(self, index):
        if len(self.__responseSheets) != 0:
            raise Exception("Изменять вопросы после начала анкетирования нельзя!")

        self.__questionnaire.down(index)

    # Получить количество ответных листов в опросе
    def getResponseSheetCount(self):
        return len(self.__responseSheets)

    # Получить ответный лист по индексу
    def getResponseSheet(self, index):
        return self.__responseSheets[index]

    # Получить список ответных листов
    def getResponseSheets(self):
        return self.__responseSheets

    # Проанализировать ответы и вернуть количество результатов, удовлетворяющих заданным условиям
    def countByParameters(self, questionIndex, age, ageInequality, gender, education, answer):
        # Если нет ни одной заполненной анкеты, вызываем исключение
        if len(self.__responseSheets) == 0:
            raise Exception("Невозможно провести анализ: для анализа нет ни одной заполненной анкеты!")

        # Проверка: переменная questionIndex должна быть типа int. Иначе выбрасывается исключение
        if type(questionIndex) is not int:
            raise TypeError("Номер вопроса должен быть числом!")

        # Проверяем индекс вопроса, по которому будет проводиться анализ
        if questionIndex < 0 or questionIndex > self.__questionnaire.getCount():
            raise Exception("Вопроса с таким индексом не существует!")

        # Проверка: переменная isPositiveAnswers должна быть типа bool. Иначе выбрасывается исключение
        if type(answer) is not bool:
            raise TypeError("Переменная isPositiveAnswers должна быть типа bool!")

        # Проверка: переменная gender должна быть типа int. Иначе выбрасывается исключение
        if type(gender) is not int:
            raise TypeError("Пол должен быть выражен целым числом! Мужчина - 1, женщина - 2, любой - 0")

        # Проверка: переменная gender должна быть в диапазоне [0, 2]. Иначе выбрасывается исключение
        if gender < 0 or gender > 2:
            raise Exception("Выход за пределы допустимых значений [0, 2]! Мужчина - 1, женщина - 2, любой - 0")

        # Функция возвращает реузультат сравнения возраста
        def ageInequalityLambda(var):
            # В зависимости от переменной ageInequality нам нужны варианты либо > age, либо < age
            if ageInequality == 1:
                return responseSheet.getAge() > age
            else:
                return responseSheet.getAge() < age

        # Количество результатов удовлетворяющих условиям
        count = 0
        # Проходимся по списку ответных листов
        for j in range(self.getResponseSheetCount()):
            responseSheet = self.getResponseSheet(j)
            # Если ответы респондента удоавлетворяет условиям, то увеличиваем переменную
            if (ageInequalityLambda(age) and responseSheet.getGender() == gender and
                responseSheet.getEducation() == education and responseSheet.getAnswer(questionIndex) == answer):
                count += 1

        return count

    # Сохранить опрос в файл. path - полное имя файла
    def saveToFile(self, path):
        # Открываем для чтения текстовый файл
        with open("{0}".format(path), "w", encoding="utf-8") as file:
            # Записываем в файл количество вопросов
            file.write("{0}\n".format(self.__questionnaire.getCount()))

            # Записываем в файл вопросы
            for i in range(self.__questionnaire.getCount()):
                file.write(self.__questionnaire.getQuestion(i) + "\n")

            # Записываем в файл ответы на анкету
            for responseSheet in self.__responseSheets:
                # Записываем возраст
                file.write("{0};".format(responseSheet.getAge()))
                # Записываем пол
                file.write("{0};".format(responseSheet.getGender()))
                # Записываем образование
                file.write("{0};".format(responseSheet.getEducation()))
                # Записываем ответы на вопросы типа да/нет
                for i in range(responseSheet.getCount()):
                    # Если это последний ответ, то записываем без точки с запятой
                    if i == responseSheet.getCount() - 1:
                        file.write("{0}\n".format(int(responseSheet.getAnswer(i))))
                    else:
                        file.write("{0};".format(int(responseSheet.getAnswer(i))))

    # Возвращает опросник, загруженный из файла. Path - полный путь к файлу
    @staticmethod
    def loadFromFile(path):
        # Открываем для чтения текстовый файл
        with open(path, encoding="utf-8") as file:
            # Создаём объект класса Опрос
            survey = Survey()
            # Считываем первую строку - число вопросов
            questionCount = int(file.readline()[:-1])
            # Считываем из файла questionCount вопросов
            for i in range(questionCount):
                # В цикле считываем строки из файла. Каждая строка - вопрос анкеты
                line = file.readline()
                # Добавляем вопрос в список, избавляясь при этом от символа конца строки, если он есть
                if line[-1] == "\n":
                    survey.addQuestion(line[:-1])
                else:
                    survey.addQuestion(line)

            # Считаем ответы на вопросы
            while True:
                # В цикле считываем строки из файла. Каждая строка - ответный лист
                line = file.readline()
                # Если все строки считаны, выходим из цикла
                if not line:
                    break
                # Разобъём строку на части
                line = line.split(";")
                # Создаём ответный лист
                responseSheet = ResponseSheet(survey.getQuestionCount())
                # Первая часть строки - это возраст респондента
                responseSheet.setAge(int(line[0]))
                # Вторая часть строки - это пол респондента
                responseSheet.setGender(int(line[1]))
                # Третья часть строки - это образование респондента
                responseSheet.setEducation(int(line[2]))
                # Остальные части - это ответы на вопросы типа да/нет
                for i in range(3, len(line)):
                    if line[i] == "0":
                        responseSheet.addAnswer(False)
                    else:
                        responseSheet.addAnswer(True)
                # Добавляем ответный лист в опросник
                survey.addResponseSheet(responseSheet)
        # Возвращаем опросник
        return survey
