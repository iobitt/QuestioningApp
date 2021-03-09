from model.SinglyLinkedList import SinglyLinkedList


# Класс Респондент
class Respondent:

    def __init__(self, name, gender, age, education):
        self.__name = None
        self.__gender = None
        self.__age = None
        self.__education = None
        self.__answers = SinglyLinkedList()

        self.setName(name)
        self.setGender(gender)
        self.setAge(age)
        self.setEducation(education)

    def __eq__(self, other):
        if type(other) is not Respondent:
            raise TypeError("Объекты должны быть одного типа!")

        if (self.getName() == other.getName() and
            self.getGender() == other.getGender() and
            self.getAge() == other.getAge() and
            self.getEducation() == other.getEducation()):
            return True
        else:
            return False

    # Установить имя респондента
    def setName(self, name):
        if type(name) is not str:
            raise TypeError("Имя должно быть выражено строкой!")

        self.__name = name

    # Установить пол респондента
    def setGender(self, gender):
        # Проверка: переменная gender должна быть типа int. Иначе выбрасывается исключение
        if type(gender) is not int:
            raise TypeError("Пол должен быть выражен целым числом! Мужчина - 1, женщина - 2")

        # Проверка: переменная gender должна быть в диапазоне [1, 2]. Иначе выбрасывается исключение
        if gender < 1 or gender > 2:
            raise ValueError("Выход за пределы допустимых значений [1, 2]! Мужчина - 1, женщина - 2")

        # Если не было брошено исключений, то присваиваем значение
        self.__gender = gender

    # Установить возраст респондента
    def setAge(self, age):
        # Проверка: переменная age должна быть типа int. Иначе выбрасывается исключение
        if type(age) is not int:
            raise TypeError("Возраст должен быть выражен целым числом!")

        # Проверка: переменная age должна быть в диапазоне [1, 150]. Иначе выбрасывается исключение
        if age < 1 or age > 150:
            raise ValueError("Выход за пределы допустимых значений возраста [1, 150]!")

        # Если не было брошено исключений, то присваиваем значение
        self.__age = age

    # Установить уровень образования респондента
    def setEducation(self, education):
        # Проверка: переменная education должна быть типа int. Иначе выбрасывается исключение
        if type(education) is not int:
            raise TypeError(
                "Уровень образования должен быть выражен целым числом! Начальное - 1, среднее - 2, высшее - 3")

        # Проверка: переменная education должна быть в диапазоне [1, 3]. Иначе выбрасывается исключение
        if education < 1 or education > 3:
            raise Exception("Выход за пределы допустимых значений [1, 3]! Начальное - 1, среднее - 2, высшее - 3")

        # Если не было брошено исключений, то присваиваем значение
        self.__education = education

    def addAnswer(self, answer):
        # if type(answer) is not Answer:
        #     raise TypeError("Входной параметр доджен быть типа Answer!")

        self.__answers.append(answer)

    def getName(self):
        return self.__name

    def getGender(self):
        return self.__gender

    def getAge(self):
        return self.__age

    def getEducation(self):
        return self.__education

    def getAnswers(self):
        return self.__answers

    def getAnswersCount(self):
        return len(self.__answers)
