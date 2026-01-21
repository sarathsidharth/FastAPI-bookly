from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from typing import List,Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

# from .book_data import books
from .schemas import Book,BookUpdateModel,BookCreateModel
from src.db.main import get_session



book_router=APIRouter()
book_service=BookService()


@book_router.get("/")
def root():
    return {"message": "Hello FastAPI"}

@book_router.get("/books",response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session)):
    books=await book_service.get_all_books(session)
    return books

@book_router.post("/create-a-book",status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_data:BookCreateModel,session:AsyncSession = Depends(get_session))-> dict:
    new_book=await book_service.create_book(book_data,session)
    return new_book

@book_router.get("/book/{book_uid}",response_model=Book)
async def get_book_by_id(book_uid:str,session:AsyncSession = Depends(get_session))-> dict:
    book = await book_service.get_book(book_uid,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not Found")

@book_router.patch("/update_book/{book_uid}",response_model=Book)
async def update_book_by_id(book_uid:str,book_update_data:BookUpdateModel,session:AsyncSession=Depends(get_session))-> dict:
    updated_book=await book_service.update_book(book_uid , book_update_data,session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")



@book_router.delete("/delete_book/{book_uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_uid:str,session:AsyncSession=Depends(get_session)):
    Delete_book= await book_service.delete_book(book_uid,session)
    if Delete_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")
    else:
        return {}