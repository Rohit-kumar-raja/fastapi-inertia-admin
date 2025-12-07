from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


# Generic Response Model
class APIResponseSchema(BaseModel, Generic[T]):
    data: Optional[T]  # This will hold the actual response model
    message: str
    success: bool = True


class LoginResponseSchema(APIResponseSchema):
    access_token: str
