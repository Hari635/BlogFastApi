from sqlalchemy import Column, Integer, String, ForeignKey
from post.database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__='blogs'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    content=Column(String)

