from typing import Optional, TypeVar
from pydantic import BaseModel


class GenericModel(BaseModel):
    id: Optional[int] = None


DBModel = TypeVar("DBModel", bound=GenericModel)


class Command(GenericModel):
    name: str
    command: str
    sequence: int
