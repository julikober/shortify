from datetime import datetime

from sqlalchemy import Column, VARCHAR, DATE, DateTime, Integer

from database.config import Base


class LinkModels(Base):
    __tablename__ = "link"
    id = Column(VARCHAR, unique=True, primary_key=True)
    url = Column(VARCHAR)
    short_url = Column(VARCHAR)
    create_time = Column(DateTime, default=datetime.utcnow())
    last_access_time = Column(DateTime, default=datetime.utcnow())
    access_count = Column(Integer, default=0)  # Changed to Integer type

    def __init__(self, id: str, url: str, short_url: str):
        self.id = id
        self.url = url
        self.short_url = short_url
        self.create_time = datetime.utcnow()
        self.last_access_time = datetime.utcnow()
        self.access_count = 0

    def __repr__(self) -> str:
        return f"<LinkModels(id={self.id}, url={self.url}, short_url={self.short_url}, create_time={self.create_time}, last_access_time={self.last_access_time}, access_count={self.access_count})>"
