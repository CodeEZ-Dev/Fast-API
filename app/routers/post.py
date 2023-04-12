from typing import Optional, List
from fastapi import FastAPI, HTTPException, status,Response,Depends,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schema,utils,oauth2
from ..database import engine,SessionLocal,get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get('/',response_model=List[schema.Post])
@router.get('/',response_model=List[schema.PostOut])
def get_all_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts""")
    # get_posts = cursor.fetchall()
    # return {"data":get_posts}
    # Below code spefic to logged in user
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #post = db.query(models.Post).limit(limit).offset(skip).all()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return result

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def creating_post(post :schema.CreatePost,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    # new_posts = cursor.fetchone()
    # conn.commit()
    # return {"data":new_posts}
    #new_posts = models.Post(title=post.title,content=post.content,published=post.published)
    new_posts = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}",response_model=schema.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # Below code spefic to logged in user
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you do not have permission to perform the action")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you do not have permission to perform the action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.Post)
def update_post(id:int,post:schema.CreatePost,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""",(post.title,post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    update_post = updated_post.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you do not have permission to perform the action")
    
    updated_post.first().update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()