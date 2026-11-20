
from beanie import Document, Indexed, PydanticObjectId
from typing import Annotated
from pydantic import BaseModel, Field

class ContactInformation(BaseModel):
    phoneNumber: str | None = None
    preferredName: str | None = None
    applicationEmail : str | None = None

class Address(BaseModel):
    street: str | None = None
    apartment: str | None = None
    city: str | None = None
    state: str | None = None
    

