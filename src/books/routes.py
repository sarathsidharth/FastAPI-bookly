from fastapi import APIRouter,status
from fastapi.exceptions import HTTPException
from typing import List,Optional

from .book_data import books
from .schemas import Book,BookUpdateModel

book_router=APIRouter()


@book_router.get("/")
def root():
    return {"message": "Hello FastAPI"}

@book_router.get("/books",response_model=List[Book])
async def get_all_books():
    return books

@book_router.post("/create-a-book",status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book)-> dict:
    new_book=book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get("/book/{book_id}")
async def get_book_by_id(book_id:int)-> dict:
    for book in books:
        if book["id"]==book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not Found")

@book_router.patch("/update_book/{book_id}")
async def update_book_by_id(book_id:int,book_update_data:BookUpdateModel)-> dict:
    for book in books:
        if book["id"]==book_id:
            book["title"]=book_update_data.title
            book["author"]=book_update_data.author
            book["publisher"]=book_update_data.publisher
            book["page_count"]=book_update_data.page_count
            book["language"]=book_update_data.language

            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")

# @book_router.patch("/update_book/{book_id}")
# async def update_book_by_id(book_id: int, book_update_data: BookUpdateModel) -> dict:
#     for book in books:
#         if book["id"] == book_id:
#             if book_update_data.title is not None:
#                 book["title"] = book_update_data.title
#             if book_update_data.author is not None:
#                 book["author"] = book_update_data.author
#             if book_update_data.publisher is not None:
#                 book["publisher"] = book_update_data.publisher
#             if book_update_data.page_count is not None:
#                 book["page_count"] = book_update_data.page_count
#             if book_update_data.language is not None:
#                 book["language"] = book_update_data.language

#             return book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id:int):
    for book in books:
        if book["id"]== book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")
