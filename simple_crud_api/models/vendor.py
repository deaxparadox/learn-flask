from sqlalchemy import Integer, String, Column, Boolean
from simple_crud_api.database import Base

    
class Vendor(Base):
    __tablename__ = "vendor"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password