from pydantic import BaseModel, Field, EmailStr,ConfigDict


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name:str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")

class GetUserResponseSchema(BaseModel):
    user: UserSchema

class CreateUserRequestSchema(BaseModel):
    """
    Структура данных для создания нового пользователя
    """
    model_config = ConfigDict(populate_by_name=True)
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")



class CreateUserResponseSchema(BaseModel):
    user: UserSchema
