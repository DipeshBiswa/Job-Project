
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
    zipCode: str | None = None
    country: str | None = None

class Education(BaseModel):
    university: str
    degree: str
    major: str
    gpa: float | None = None
    startDate: str | None = None
    graduationDate: str | None = None

class WorkExprience(BaseModel):
    company: str
    jobTitle: str
    location: str | None = None
    startDate: str | None = None
    endDate: str | None = None
    currentlyWorking: bool = False
    description: str | None = None

class ProfessionalLinks(BaseModel):
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None

class WorkEligibility(BaseModel):
    authorizedToWork: bool | None = None
    requiredSponsorship: bool | None = None
    willingToRelocate: bool | None = None


class Profile(Document):
    userId: Annotated[PydanticObjectId, Indexed(unique = True)]

    contactInformation: ContactInformation = Field(default_factory = ContactInformation)
    address: Address = Field(default_factory=Address)

    education: list[Education] = Field(default_factory=list)

    workExperience: list[WorkExprience] = Field(default_factory=list)

    skills: list[str] = Field(default_factory=list)

    professionalLinks: ProfessionalLinks = Field(
        default_factory=ProfessionalLinks
    )

    workEligibility: WorkEligibility = Field(
        default_factory=WorkEligibility
    )
class Settings:
    name = "profiles"



