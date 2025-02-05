from sqlalchemy import Integer, String, Column, Boolean, Enum
from simple_crud_api.database import Base

from ..utils.user import UserType

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    type = Column(Enum(UserType), default=UserType.Employee)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    