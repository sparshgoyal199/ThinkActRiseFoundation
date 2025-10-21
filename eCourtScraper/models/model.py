from sqlmodel import SQLModel,Field
from pydantic import StringConstraints
from typing_extensions import Annotated

stateNameType = Annotated[str, StringConstraints(strip_whitespace=True)]
#pydantic level constraints

class statecodes(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    stateName: stateNameType = Field(unique=True)
    #through field we define database level constraints
    stateCode: int = Field(unique=True)
    
    