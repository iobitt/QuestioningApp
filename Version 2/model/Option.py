# Вариант ответа анкеты
class Option:

    def __init__(self, ID, value, weight):
        self.__id = None
        self.__value = None
        self.__weight = None

        self.setId(ID)
        self.setValue(value)
        self.setWeight(weight)

    def setId(self, ID):
        if type(ID) is not int:
            raise TypeError("id должен быть выражен целым числом!")

        if ID < 0:
            raise ValueError("id должен быть не отрицательным числом!")

        # Если не было брошено исключений, то присваиваем значение
        self.__id = ID

    # Установить значение
    def setValue(self, value):
        if type(value) is not str:
            raise TypeError("value must be str!")

        if not len(value):
            raise TypeError("Строка не должна быть пустой!")

        self.__value = value

    def setWeight(self, weight):
        if type(weight) is not int:
            raise TypeError("Вес должен быть выражен целым числом!")

        if weight < 0:
            raise ValueError("Вес должен быть не отрицательным числом!")

        self.__weight = weight

    def getId(self):
        return self.__id

    def getValue(self):
        return self.__value

    def getWeight(self):
        return self.__weight