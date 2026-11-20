from pydantic import BaseModel, Field

from app.Model.profile import (
    ContactInformation,
    Address,
    Education,
    WorkExprience,
    ProfessionalLinks,
    WorkEligibility
)

class ProfileCreate(BaseModel):
    contactInformation: ContactInformation = Field(default_factory=ContactInformation)

    address: Address = Field(default_factory = Address)

    education: list[Education] = Field(default_factory = list)

    workExprience: list[WorkExprience] = Field(default_factory = list)

    skills: list[str] = Field(default_factory = list)
    professionalLinks: ProfessionalLinks = Field(default_factory = ProfessionalLinks)

    workEligibility: WorkEligibility = Field(default_factory=WorkEligibility)

class ProfileResponse(ProfileCreate):
    id: str