from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(
        min_length=12,
        max_length=128,
    )
    from pydantic import BaseModel, ConfigDict, EmailStr


from app.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    role: UserRole
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
