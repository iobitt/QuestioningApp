# Импортируем Односвязный список
from model.SinglyLinkedList import SinglyLinkedList


# Класс Ответный лист. Содержит ответы на вопросы на анкеты
class ResponseSheet:

    def __init__(self, count):
        # Проверка: переменная count должна быть типа int и > 0. Иначе выбрасывается исключение
        if type(count) is not int or count < 1:
            raise TypeError("Количество вопросов должно быть целым положительным числом!")

        # Возраст респондента
        self.__age = None
        # Пол респондента
        self.__gender = None
        # Уровень образования респондента
        self.__education = None
        # Ответы на вопросы типа да/нет
        self.__answers = SinglyLinkedList()
        # На сколько вопросов типа да/нет нужно ответить
        self.__maxCount = count

    # Установить возраст респондента
    def setAge(self, age):
        # Проверка: переменная age должна быть типа int. Иначе выбрасывается исключение
        if type(age) is not int:
            raise TypeError("Возраст должен быть выражен целым числом!")

        # Проверка: переменная age должна быть в диапазоне [1, 150]. Иначе выбрасывается исключение
        if age < 1 or age > 150:
            raise Exception("Выход за пределы допустимых значений возраста [1, 150]!")

        # Если не было брошено исключений, то присваиваем значение
        self.__age = age

    # Установить пол респондента
    def setGender(self, gender):
        # Проверка: переменная gender должна быть типа int. Иначе выбрасывается исключение
        if type(gender) is not int:
            raise TypeError("Пол должен быть выражен целым числом! Мужчина - 1, женщина - 2")

        # Проверка: переменная gender должна быть в диапазоне [1, 2]. Иначе выбрасывается исключение
        if gender < 1 or gender > 2:
            raise Exception("Выход за пределы допустимых значений [1, 2]! Мужчина - 1, женщина - 2")

        # Если не было брошено исключений, то присваиваем значение
        self.__gender = gender

    # Установить уровень образования респондента
    def setEducation(self, education):
        # Проверка: переменная education должна быть типа int. Иначе выбрасывается исключение
        if type(education) is not int:
            raise TypeError("Уровень образования должен быть выражен целым числом! Начальное - 1, среднее - 2, высшее - 3")

        # Проверка: переменная education должна быть в диапазоне [1, 3]. Иначе выбрасывается исключение
        if education < 1 or education > 3:
            raise Exception("Выход за пределы допустимых значений [1, 3]! Начальное - 1, среднее - 2, высшее - 3")

        # Если не было брошено исключений, то присваиваем значение
        self.__education = education

    # Добавить ответ на вопрос типа Да/Нет
    def addAnswer(self, answer):
        # Проверка: переменная answer должна быть типа bool. Иначе выбрасывается исключение
        if type(answer) is not bool:
            raise TypeError("Входной параметр должен быть типа bool!")

        # Проверка: есть ли не отвеченные вопросы типа да/нет
        if self.__maxCount == len(self.__answers):
            raise Exception("Вы уже ответили на все вопросы!")

        # Если не было брошено исключений, то добавляем элемент в список
        self.__answers.append(answer)

    # Получить возраст респондента
    def getAge(self):
        # Проверка: задан ли возраст
        if self.__age is None:
            raise Exception("Возраст не задан!")
        # Возвращает возраст
        return self.__age

    # Получить пол респондента
    def getGender(self):
        # Проверка: задан ли пол
        if self.__gender is None:
            raise Exception("Пол не задан!")
        # Возвращает пол
        return self.__gender

    # Получить образование респондента
    def getEducation(self):
        # Проверка: задано ли образование
        if self.__education is None:
            raise Exception("Образование не задано!")
        # Возвращает образование
        return self.__education

    # Получить количество вопросов типа да/нет, на которые был дан ответ
    def getCount(self):
        return len(self.__answers)

    # Получить общее количество вопросов
    def getMaxCount(self):
        return self.__maxCount

    # Получить ответ на вопрос
    def getAnswer(self, index):
        return self.__answers[index]

    # Изменить ответ на вопрос
    def changeAnswer(self, answer, index):
        # Проверка: переменная answer должна быть типа bool. Иначе выбрасывается исключение
        if type(answer) is not bool:
            raise TypeError("Входной параметр должен быть типа bool!")

        self.__answers[index] = answer

    # Возвращает True, если на все вопросы дан ответ
    def isAllReplyReceived(self):
        if self.__age is None:
            raise Exception("Возраст не задан!")

        if self.__gender is None:
            raise Exception("Пол не задан!")

        if self.__education is None:
            raise Exception("Образование не задано!")

        if self.__maxCount != len(self.__answers):
            raise Exception("Вы не ответили на все вопросы типа да/нет!")

        return True