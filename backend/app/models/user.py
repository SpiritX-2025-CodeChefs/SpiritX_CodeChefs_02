from pydantic import BaseModel, validator
import re


class UserRegister(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 8:
            raise ValueError("Username must be at least 8 characters long")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UsernameCheck(BaseModel):
    username: str
