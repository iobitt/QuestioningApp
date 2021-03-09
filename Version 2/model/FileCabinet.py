from model.SinglyLinkedList import SinglyLinkedList
from model.Profile import Profile
import pickle


# Класс Картотека
class FileCabinet:

    def __init__(self):
        self.__profiles = SinglyLinkedList()
        self.__password = ""
        self.__access = set()

    def setAccess(self, access):
        self.__access = access

    def checkPermissions(self, value):
        return value in self.__access

    def setPassword(self, value):
        if type(value) is not str:
            raise TypeError("Название вопроса должно быть выражено строкой!")

        self.__password = value

    def addProfile(self, profile):
        if type(profile) is not Profile:
            raise TypeError("Входной параметр доджен быть типа Profile!")

        self.__profiles.append(profile)

    def getPassword(self):
        return self.__password

    def getProfiles(self):
        return self.__profiles

    def getProfilesCount(self):
        return len(self.__profiles)

    @staticmethod
    def save(path, fileCabinet):
        if type(fileCabinet) is not FileCabinet:
            raise TypeError("Входной параметр доджен быть типа FileCabinet!")

        with open(path, 'wb') as file:
            pickle.dump(fileCabinet, file)

    @staticmethod
    def load(path):
        with open(path, 'rb') as file:
            fileCabinet = pickle.load(file)

            if type(fileCabinet) is not FileCabinet:
                raise TypeError("Загруженный объект имеет неверный тип!")

        return fileCabinet

    def deleteProfile(self, index):
        self.__profiles.delete(index)
