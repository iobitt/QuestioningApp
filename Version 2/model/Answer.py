# Ответ на вопрос анкеты
class Answer:

    def __init__(self, value, weight):
        self.__value = None
        self.__weight = None

        self.setValue(value)
        self.setWeight(weight)

    # Установить значение
    def setValue(self, value):
        if type(value) is not tuple:
            raise TypeError("value must be tuple!")

        if not len(value):
            raise TypeError("Ответ не должен быть пустым!")

        self.__value = value

    def setWeight(self, weight):
        if type(weight) is not int:
            raise TypeError("Вес должен быть выражен целым числом!")

        if weight < 0:
            raise ValueError("Вес должен быть не отрицательным числом!")

        self.__weight = weight

    def getValue(self):
        return self.__value

    def getWeight(self):
        return self.__weight
