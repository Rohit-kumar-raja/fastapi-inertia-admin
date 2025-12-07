from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Generic, TypeVar, Optional


class BaseSchema(BaseModel):
    is_active: bool = Field(True, description="Indicates if the resource is active")
    # created_at: datetime | None = Field(None, description="Timestamp of creation")
    # updated_at: datetime | None = Field(None, description="Timestamp of last update")
    # deleted_at: datetime | None = Field(None, description="Timestamp of soft deletion, if applicable")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


T = TypeVar("T")


# Generic Response Model
class APIResponseSchema(BaseModel, Generic[T]):
    data: Optional[T]  # This will hold the actual response model
    message: str
    success: bool = True


class APIResponseErrorSchema(BaseModel):
    message: str
    success: bool = False
