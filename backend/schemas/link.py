from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl

# Link Schema
class Base(BaseModel):
    id: str
    url: str
    short_url: str
    create_time: datetime
    last_access_time: datetime
    access_count: int
    
    class Config:
        orm_mode = True

class Create(BaseModel):
    url: HttpUrl
    custom_id: Optional[str] = None

class Update(BaseModel):
    url: HttpUrl

class Analytics(BaseModel):
    id: str
    url: str
    short_url: str
    access_count: int
    create_time: datetime
    last_access_time: datetime
