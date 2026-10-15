
class User:
    def __init__(self, firstName, lastName, email, password):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__password = password

    def getFirstName(self):
        return self.__firstName
    def getLastName(self):
        return self.__lastName
    def getEmail(self):
        return self.__email
    
    def setFirstName(self, firstName):
        self.__firstName = firstName
    def setLastName(self, lastName):
        self.__lastName = lastName
    def setEmail(self, email):
        self.__email = email

