
from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from post import schemas,database,models
from sqlalchemy.orm import Session
import string
import random

def generate_unique_code(db: Session):
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        blog=db.query(models.Blog).filter(models.Blog.id==code).first()
        if not blog:
            break

    return code


router=APIRouter(
    prefix="/blogposts",
    tags=['Post']
)

get_db=database.get_db

@router.get('/',response_model=List[schemas.BlogBase])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    # id=generate_unique_code(db)
    new_blog=models.Blog(title=request.title,content=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', status_code=200, response_model=schemas.BlogBase)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not available")
    return blog

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if( not blog.first()):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.update({models.Blog.title: request.title}, synchronize_session=False)
    blog.update({models.Blog.content: request.content}, synchronize_session=False)

    db.commit()
    return 'updated'

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'
