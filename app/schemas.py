from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

# authentication
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# event manage
class EventCreate(BaseModel):
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str
    
class EventOut(BaseModel):
    id: int
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str
    
    class Config:
        orm_mode = True

# telegram bot
class CCCDInfo(BaseModel):
    identityCode: str
    name: str
    dob: str
    gender: str

class ContactCreate(BaseModel):
    isAppointment: bool
    appointmentTime: str
    department: str
    phoneNumber: str
    note: str
    cccdInfo: CCCDInfo
