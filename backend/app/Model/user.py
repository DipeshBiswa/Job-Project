from beanie import Document, Indexed
from typing import Annotated

class User(Document):
    firstName: str
    lastName: str
    email: Annotated[str, Indexed(unique=True)]
    password_hash: str

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getEmail(self):
        return self.email

    def setFirstName(self, firstName: str):
        self.firstName = firstName

    def setLastName(self, lastName: str):
        self.lastName = lastName

    def setEmail(self, email: str):
        self.email = email

    class Settings:
        name = "users"