# Реализация односвязного списка
class SinglyLinkedList:

    def __init__(self):
        # Количество элементов в списке
        self.count = 0
        # Ссылка на первый элемент списка
        self.firstElement = None

    # Добавляет элемент в конец списка
    def append(self, value):
        # Создаём из входного значения элемент односвязного списка
        el = ListElement(value)
        # Если список пуст(firstElement ссылается на None)
        if self.firstElement is None:
            # То первый элемент будет ссылаться на этот элемент
            self.firstElement = el
        else:
            # Иначе находим последний элемент списка
            lastElement = self.getLastElement()
            # Теперь последний элемент будет ссылаться на только что добавленный элемент
            lastElement.nextEl = el
        # Увеличиваем количество элементов в списке
        self.count += 1

    # Добавляет элемент в начало списка
    def appendLeft(self, value):
        # Создаём из входного значения элемент односвязного списка
        el = ListElement(value)
        # Если список пуст(firstElement ссылается на None)
        if self.firstElement is None:
            # То первый элемент будет ссылаться на этот элемент
            self.firstElement = el
        else:
            # el получает ссылку на текущий первый элемент списка
            el.nextEl = self.firstElement
            # Первым элементом списка становится el
            self.firstElement = el
        # Увеличиваем количество элементов в списке
        self.count += 1

    # Удалить элемент по индексу
    def delete(self, index):
        # Если index не является целым числом, то выбрасываем исключение
        if type(index) is not int:
            raise TypeError("list indices must be integers or slices, not str")

        # Если index выходит за предел допустимых значений, то выбрасываем исключение
        if index >= self.count or index < 0:
            raise IndexError("list index out of range")

        # Если список пуст, то выбрасываем исключение
        if self.count == 0:
            raise Exception("Список пуст!")
        # Если нужно удалить первый элемент
        if index == 0:
            # То первым элементом будет тот элемент, на который сейчас ссылается текущий элемент
            self.firstElement = self.firstElement.nextEl
            # Уменьшаем количество элементов в списке
            self.count -= 1
        # Если нужно удалить не первый элемент
        else:
            # Получаем предыдущий элемент
            backEl = self.__getItem(index - 1)
            # Получаем текущий элемент
            el = self.__getItem(index)
            # Следующим за предыдущим элементом делаем следующий после текущего
            backEl.nextEl = el.nextEl
            # Уменьшаем количество элементов в списке
            self.count -= 1

    # Расширить список list, добавляя в конец все элементы списка L
    def extend(self, L):
        for i in L:
            self.append(i)

    # Вернуть последний элемент списка
    def getLastElement(self):
        # Если длина списка равна 0, то возвращается None
        if self.count == 0:
            return None
        else:
            # Переменной el присваиваем первый элемент списка
            el = self.firstElement
            # Каждый элемент списка содержит ссылку на следующий элемент. В цикле дойдём до последнего элемента
            while True:
                # Если следующий элемент None, значит el и является последним элементом. Возвращаем его
                if el.nextEl is None:
                    return el
                else:
                    # Иначе, в el присваиваем элемент, следующий за el
                    el = el.nextEl

    # Вернуть элемент по индексу
    def __getItem(self, index):
        # Если index не является целым числом, то выбрасываем исключение
        if type(index) is not int:
            raise TypeError("list indices must be integers or slices, not str")

        # Если index выходит за предел допустимых значений, то выбрасываем исключение
        if index >= self.count or index < 0:
            raise IndexError("list index out of range")

        # Переменной el присваиваем первый элемент списка
        el = self.firstElement
        # Переменная для перебора списка
        i = 0
        # Каждый элемент списка содержит ссылку на следующий элемент. В цикле будем перебирать элементы, пока не найдём элемент с нужным индексом
        while True:
            # Если элемент с нужным индексом, возвращаем его
            if i == index:
                return el
            else:
                # Иначе, в el присваиваем элемент, следующий за el
                el = el.nextEl
                # Увеличиваем счётчик на единицу
                i += 1

    # Перегрузка оператора доступ по индексу
    def __getitem__(self, index):
        # Получаем элемент с нужным индексом, затем возращается полезная составляющая
        return self.__getItem(index).data

    # Перегрузка оператора присвоения значения по индексу
    def __setitem__(self, index, value):
        # Если index не является целым числом, то выбрасываем исключение
        if type(index) is not int:
            raise TypeError("list indices must be integers or slices, not str")

        # Если index выходит за предел допустимых значений, то выбрасываем исключение
        if index >= self.count or index < 0:
            raise IndexError("list index out of range")

        # Переменной el присваиваем первый элемент списка
        el = self.firstElement
        # Переменная для перебора списка
        i = 0
        # Каждый элемент списка содержит ссылку на следующий элемент. В цикле будем перебирать элементы, пока не найдём элемент с нужным индексом
        while True:
            # Если элемент с нужным индексом, возвращаем его
            if i == index:
                el.data = value
                return
            else:
                # Иначе, в el присваиваем элемент, следующий за el
                el = el.nextEl
                # Увеличиваем счётчик на единицу
                i += 1

    # Перегрузка метода для функции len()
    def __len__(self):
        return self.count

    # Перегрузка функции Строковое представление объекта
    def __str__(self):
        # Возвращаемая строка
        output = "["
        # Получаем первый элемент
        el = self.firstElement
        # Если он равен None, то возвращаем строку с пустыми скобками
        if el is None:
            return "[]"
        # В бесконечном циклн
        while True:
            # Добавляем элемент в строку через запятую
            output += str(el.data) + ", "
            # Если этот элемент последний, то выходим из цикла
            if el.nextEl is None:
                break
            # Иначе текущим элементом становится следующий элемент
            else:
                el = el.nextEl
        # Возвращаем получившуюся строку
        return output[:-2] + "]"

    # Перегрузка оператора +=
    def __iadd__(self, other):
        # Расширяем текущий список вторым списком
        self.extend(other)
        return self

    # Полностью отчищает список
    def clear(self):
        # Количество элементов в списке
        self.count = 0
        # Ссылка на первый элемент списка
        self.firstElement = None


# Элемент односвязного списка
class ListElement:

    def __init__(self, data):
        # Ссылка на следующий элемент
        self.nextEl = None
        # Объект совершенно любого класса. Значение присваивается в конструторе при создании объекта ListElement
        self.data = data
