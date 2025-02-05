from sqlalchemy import Integer, String, Column

from .database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class Vendor(Base):
    __tablename__ = "vendor"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password