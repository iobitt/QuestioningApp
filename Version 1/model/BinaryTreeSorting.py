# Импортируем Односвязный список
from model.SinglyLinkedList import SinglyLinkedList


# Вершина бинарного дерева
class Top:

    def __init__(self, value):
        # Данные
        self.__value = value
        # Левый потомок
        self.__left = None
        # Правый потомок
        self.__right = None

    # Устаналиваем значение левому потомку
    def setLeft(self, value):
        self.__left = value

    # Устаналиваем значение правому потомку
    def setRight(self, value):
        self.__right = value

    # Получить значение вершины
    def getValue(self):
        return self.__value

    # Получить ссылку на левого потомка
    def getLeft(self):
        return self.__left

    # Получить ссылку на правого потомка
    def getRight(self):
        return self.__right


# Класс предоставляет статический метод сортировки бинарным деревом
class BinaryTreeSorting:

    # Функция принимает на вход список и сортирует его
    @staticmethod
    def sort(inputList, key=lambda val: val):
        # Проходим по элементам списка
        for i, el in enumerate(inputList):
            # Первый элемент списка будет первой вершиной бинарного дерева
            if i == 0:
                firstTop = Top(el)
            else:
                # Изначально текущей вершиной делаем первую вершину
                currentTop = firstTop
                while True:
                    # Если элемент из списка больше или равен текущей вершине, то переходим к правому потомку текущей вершины
                    if key(el) >= key(currentTop.getValue()):
                        # Если правый потомок не существует, то им станет текущий элемент списка. Цикл завершается
                        if currentTop.getRight() is None:
                            currentTop.setRight(Top(el))
                            break
                        # Иначе текущей вершиной становиться правый потомок. Возвращаемся к началу цикла
                        else:
                            currentTop = currentTop.getRight()
                    # Иначе переходим к левому потомку текущей вершины
                    else:
                        # Если левый потомок не существует, то им станет текущий элемент списка. Цикл завершается
                        if currentTop.getLeft() is None:
                            currentTop.setLeft(Top(el))
                            break
                        # Иначе текущей вершиной становиться левый потомок. Возвращаемся к началу цикла
                        else:
                            currentTop = currentTop.getLeft()
        # Отчищаем входной список
        inputList.clear()
        # Из бинарного дерева формируем список и присваиваем его входному списку
        inputList += BinaryTreeSorting.__getListOfTopChild(firstTop)

    # Получить список потомков вершины бинарного дерева. top - вершина бинарного дерева
    @staticmethod
    def __getListOfTopChild(top):
        # Проверка: переменная top должна быть типа Top. Иначе выбрасывается исключение
        if type(top) is not Top:
            raise TypeError("Вершина должна иметь тип Top!")

        # Создаём список
        output = SinglyLinkedList()
        # Если левый потомок вершины тоже вершина, то рекурсивно вызываем эту функцию для левого потомка
        if top.getLeft() is not None:
            # Результат заносим в список
            output += BinaryTreeSorting.__getListOfTopChild(top.getLeft())
        # Заносим в список значение текущей вершины
        output.append(top.getValue())
        # Если правый потомок вершины тоже вершина, то рекурсивно вызываем эту функцию для правого потомка
        if top.getRight() is not None:
            # Результат заносим в список
            output += BinaryTreeSorting.__getListOfTopChild(top.getRight())
        # Возвращаем список
        return output
