from typing import List,Optional
from pydantic import BaseModel

class BlogBase(BaseModel):
    id:int
    title:str
    content:str

    class Config():
	    orm_mode=True

class createBlog(BaseModel):
    title:str
    content:str

class Blog(createBlog):
    class Config():
        orm_mode = True
