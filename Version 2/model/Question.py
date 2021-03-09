from model.SinglyLinkedList import SinglyLinkedList


# Класс Вопрос анкеты
class Question:

    def __init__(self, heading, hint, type, weight):
        self.__heading = None
        self.__hint = None
        self.__type = None
        self.__weight = None
        self.__options = SinglyLinkedList()

        self.setHeading(heading)
        self.setHint(hint)
        self.setType(type)
        self.setWeight(weight)

    def __str__(self):
        line = ""
        line += "Заголовок вопроса: " + self.__heading + "\n"
        line += "Подзаголовок вопроса: " + self.__hint + "\n"
        line += "Тип вопроса: " + str(self.__type) + "\n"
        line += "Вес вопроса: " + str(self.__weight) + "\n"
        line += "Варианты ответа:" + "\n"
        for index, option in enumerate(self.__options):
            line += str(index + 1) + ". " + option + "\n"
        return line

    def setHeading(self, value):
        if type(value) is not str:
            raise TypeError("Название вопроса должно быть выражено строкой!")

        if not len(value):
            raise TypeError("Заголовок вопроса не должен быть пустой строкой!")

        self.__heading = value

    def setHint(self, value):
        if type(value) is not str:
            raise TypeError("Подсказка к вопросу должна быть выражена строкой!")

        self.__hint = value

    def setType(self, value):
        if type(value) is not int:
            raise TypeError("Тип вопроса должен быть выражен целым числом!")

        if value < 1 or value > 3:
            raise ValueError("Выход за пределы допустимых значений типа [1, 3]!")

        # Если не было брошено исключений, то присваиваем значение
        self.__type = value

    def setWeight(self, weight):
        if type(weight) is not int:
            raise TypeError("Вес должен быть выражен целым числом!")

        if weight < 0:
            raise ValueError("Вес должен быть не отрицательным числом!")

        self.__weight = weight

    def addOption(self, option):
        if type(option) is not str:
            raise TypeError("Входной параметр доджен быть типа str!")

        self.__options.append(option)

    def getHeading(self):
        return self.__heading

    def getHint(self):
        return self.__hint

    def getType(self):
        return self.__type

    def getWeight(self):
        return self.__weight

    def getOptions(self):
        return self.__options

    # Поднять вариант ответа в списке
    def optionUp(self, index):
        if index == 0:
            raise OptionNotUpOrDownExc("Вопрос и так стоит на самой верхней позиции!")

        # Меняем местами элементы
        self.__options[index], self.__options[index - 1] = self.__options[index - 1], self.__options[index]

    # Опустить вариант ответа в списке
    def optionDown(self, index):
        if index == len(self.__options) - 1:
            raise OptionNotUpOrDownExc("Вопрос и так стоит на самой нижней позиции!")

        # Меняем местами элементы
        self.__options[index], self.__options[index + 1] = self.__options[index + 1], self.__options[index]

    # Удалить вариант ответа
    def deleteOption(self, index):
        self.__options.delete(index)


# Исключение. Нельзя поднять или опустить вариант ответа в вопросе
class OptionNotUpOrDownExc(Exception):

    def __init__(self, text):
        self.txt = text