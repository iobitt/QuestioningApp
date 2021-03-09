# Импортируем Односвязный список
from model.SinglyLinkedList import SinglyLinkedList


# Класс Вопросник. Содержит вопросы для анкетирования
class Questionnaire:

    def __init__(self):
        # Список с вопросами
        self.__questions = SinglyLinkedList()

    # Добавить вопрос
    def addQuestion(self, question):
        # Проверка: переменная question должна быть типа string и иметь не нулевую длину. Иначе выбрасывается исключение
        if type(question) is not str or len(question) < 1:
            raise TypeError("Вопрос должен быть не пустой строкой!")

        # Если не было брошено исключений, то добавляем элемент в список
        self.__questions.append(question)

    # Получить вопрос по индексу
    def getQuestion(self, index):
        return self.__questions[index]

    # Заменить вопрос
    def changeQuestion(self, question, index):
        # Проверка: переменная question должна быть типа string. Иначе выбрасывается исключение
        if type(question) is not str:
            raise TypeError("Вопрос должен быть строкой!")

        self.__questions[index] = question

    # Удалить вопрос
    def deleteQuestion(self, index):
        self.__questions.delete(index)

    # Получить количество добавленных вопросов
    def getCount(self):
        return len(self.__questions)

    # Поднять вопрос в списке
    def up(self, index):
        if index == 0:
            raise Exception("Вопрос и так стоит на самой верхней позиции!")

        # Меняем местами элементы
        self.__questions[index], self.__questions[index - 1] = self.__questions[index - 1], self.__questions[index]

    # Опустить вопрос в списке
    def down(self, index):
        if index == self.getCount() - 1:
            raise Exception("Вопрос и так стоит на самой нижней позиции!")

        # Меняем местами элементы
        self.__questions[index], self.__questions[index + 1] = self.__questions[index + 1], self.__questions[index]
