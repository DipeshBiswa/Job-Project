
class User:
    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def getFirstName(self):
        return self.firstName
    def getLastName(self):
        return self.lastName
    def getEmail(self):
        return self.email
    
    def setFirstName(self, firstName):
        self.firstName = firstName
    def setLastName(self, lastName):
        self.lastName = lastName
    def setEmail(self, email):
        self.email = email
        
    