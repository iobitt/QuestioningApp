from model.SinglyLinkedList import SinglyLinkedList
from model.Question import Question
from model.Respondent import Respondent


# Анкета
class Profile:

    def __init__(self, name, description):
        self.__name = None
        self.__description = None
        self.__questions = SinglyLinkedList()
        self.__respondents = SinglyLinkedList()

        self.setName(name)
        self.setDescription(description)

    def setName(self, name):
        if type(name) is not str:
            raise TypeError("name must be str")

        if not len(name):
            raise TypeError("Строка не должна быть пустой!")

        self.__name = name

    def setDescription(self, description):
        if type(description) is not str:
            raise TypeError("description must be str")

        if not len(description):
            raise TypeError("Строка не должна быть пустой!")

        self.__description = description

    def addQuestion(self, question):
        if type(question) is not Question:
            raise TypeError("Входной параметр доджен быть типа Question!")

        self.__questions.append(question)

    def addRespondent(self, respondent):
        if type(respondent) is not Respondent:
            raise TypeError("Входной параметр доджен быть типа Respondent!")

        self.__respondents.append(respondent)

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getQuestions(self):
        return self.__questions

    def getRespondents(self):
        return self.__respondents

    def getQuestionsCount(self):
        return len(self.__questions)

    def getRespondentsCount(self):
        return len(self.__respondents)

    def getAnalyseData(self):
        data = {}
        data['name'] = self.getName()
        data['questions'] = []
        for index, item in enumerate(self.getQuestions()):
            question = {}
            question['heading'] = item.getHeading()
            question['type'] = item.getType()

            if question['type'] == 2 or question['type'] == 3:
                respondentCount = self.getRespondentsCount()
                # Счётчик ответов
                responseСounter = {}
                for option in item.getOptions():
                    responseСounter[option] = 0

                # Проходим по ответам и увеличиваем счётчик
                for respondent in self.getRespondents():
                    answer = respondent.getAnswers()[index]
                    for answerPart in answer:
                        try:
                            responseСounter[answerPart] += 1
                        except KeyError:
                            pass

                values = [[], [], []]

                for key in responseСounter:
                    values[0].append(key)
                    values[1].append(responseСounter[key])
                    try:
                        values[2].append(responseСounter[key] * 100 / respondentCount)
                    except ZeroDivisionError:
                        values[2].append(0)

                question['values'] = values
            else:
                question['values'] = []
                for respondent in self.getRespondents():
                    answers = respondent.getAnswers()
                    question['values'].append(answers[index][0])
            data['questions'].append(question)
        return data

    def getDataForGeneralTable(self):
        data = [["Вопрос"], ["Тип вопроса"], ["Варианты ответа"]]
        for question in self.__questions:
            data[0].append(question.getHeading())
            qType = question.getType()
            if qType == 1:
                data[1].append("Текстовый")
            elif qType == 2:
                data[1].append("Одиночный выбор")
            else:
                data[1].append("Множественный выбор")

            options = ""
            for option in question.getOptions():
                options += option + ", "
            data[2].append(options[:-2])

        for index, respondent in enumerate(self.__respondents):
            column = []
            column.append("Респондент " + str(index + 1))
            for answer in respondent.getAnswers():
                answers = ""
                for part in answer:
                    answers += part + ", "
                column.append(answers[:-2])
            data.append(column)
        return data

    def getDataForGeneralTable2(self):
        data = {}
        data['headings'] = ["Вопрос", "Тип вопроса", "Варианты ответа"]
        data['body'] = []

        for i in range(len(self.__respondents)):
            data['headings'].append("Респондент " + str(i + 1))

        for qIndex, question in enumerate(self.__questions):
            line = []

            line.append(question.getHeading())

            qType = question.getType()
            if qType == 1:
                line.append("Текстовый")
            elif qType == 2:
                line.append("Одиночный выбор")
            else:
                line.append("Множественный выбор")

            options = ""
            for option in question.getOptions():
                options += option + ", "
            line.append(options[:-2])

            for index, respondent in enumerate(self.__respondents):
                answers = ""
                answer = respondent.getAnswers()[qIndex]
                for part in answer:
                    answers += part + ", "
                line.append(answers[:-2])
            data['body'].append(line)
        return data

    # Поднять вопрос в списке
    def questionUp(self, index):
        if index == 0:
            raise QuestionNotUpOrDownExc("Вопрос и так стоит на самой верхней позиции!")

        # Меняем местами вопросы
        self.__questions[index], self.__questions[index - 1] = self.__questions[index - 1], self.__questions[index]

        # Меняем местами ответы
        for respondent in self.__respondents:
            answers = respondent.getAnswers()

            answers[index], answers[index - 1] = answers[index - 1], answers[index]

    # Опустить вопрос в списке
    def questionDown(self, index):
        if index == len(self.__questions) - 1:
            raise QuestionNotUpOrDownExc("Вопрос и так стоит на самой нижней позиции!")

        # Меняем местами элементы
        self.__questions[index], self.__questions[index + 1] = self.__questions[index + 1], self.__questions[index]

        # Меняем местами ответы
        for respondent in self.__respondents:
            answers = respondent.getAnswers()

            answers[index], answers[index + 1] = answers[index + 1], answers[index]

    # Удалить вариант ответа
    def deleteQuestion(self, index):
        self.__questions.delete(index)

        # Удаляем ответы
        for respondent in self.__respondents:
            answers = respondent.getAnswers()
            answers.delete(index)


# Исключение. Нельзя поднять или опустить вопрос
class QuestionNotUpOrDownExc(Exception):

    def __init__(self, text):
        self.txt = text