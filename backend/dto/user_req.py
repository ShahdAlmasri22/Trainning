from pydantic import BaseModel, EmailStr, field_validator, Field
import re

class user_request(BaseModel):
    name: str
    email: EmailStr
    password:str= Field(...,min_length=6, max_length=20)

    @field_validator("password")
    def password_strength(cls, passw):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[*&]).{6,}$"
        if not re.match(pattern, passw):
            raise ValueError(
               """Password must be at least 6 characters contain: at least one letter, 
                  one number, and one special character: * or &"""
            )
        return passw


class login(BaseModel):
    email: EmailStr
    password: str


class profile(BaseModel):
    name: str | None = None
    old_password: str | None = None
    new_password: str | None = None

    @field_validator("new_password")
    def password_strength(cls, passw):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[*&]).{6,}$"
        if not re.match(pattern, passw):
            raise ValueError(
                """Password must be at least 6 characters contain: at least one letter, 
                   one number, and one special character: * or &"""
            )
        return passw