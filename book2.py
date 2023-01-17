
from typing import Optional
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

app = FastAPI()

class BaseUsers(BaseModel):
    name: str
    lastname:str
    email: EmailStr

class UserOut(BaseUsers):
    password: str


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length= 1)
    author: str = Field (max_length=100, min_length= 2 )
    description: Optional [str] = Field(title= "Description of Book")
    rating: int = Field(gt=-1, lt=101)

class Book_no_rating(BaseModel):
    id: UUID
    title: str = Field(min_length= 1)
    author: str = Field (max_length=100, min_length= 2 )
    description: Optional [str] = Field(title= "Description of Book")


    class Config:
        schema_extra =  {

            "example" :{
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "Title of Book here",
                "author": "book authores name",
                "description": "summary of what the book entails",
                "rating": 45

            }

        }




Books = []

@app.get("/")
async def get_all_books():
    if len(Books) < 1:
        auto_create_book()
    return Books

@app.get("/book/{book_id}")
async def get_book(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x
    raise http_exception()

@app.get("/book/rating/{book_id}", response_model= Book_no_rating)
async def get_book_no_rating(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x
    raise http_exception()

@app.post("/", status_code= status.HTTP_201_CREATED)
async def add_book(book: Book):
    Books.append(book)

    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    
    counter = 0
    for x in Books:
        counter += 1
        if x.id == book_id:
            Books[counter -1] = book
            return Books[counter -1] 
    raise http_exception()

    

@app.delete("/{book_id}")
async def delete_book(book_id:UUID):
    counter = 0
    for x in Books:
        counter += 1
        if x.id == book_id:
            del Books[counter -1]
            return f"id {book_id} deleted"
    raise http_exception()


@app.post("/user/")
async def createuser(users: UserOut) -> BaseUsers:
    return users






















def auto_create_book():

    book1  = Book(id =  "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  title = "Atomic Habit",
                  author = "Unkown",
                  description = "A self Motivation book for youths",
                  rating =  60)
    

    book2  = Book(id =  "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                  title = "Python Crash Course",
                  author = "Unkown",
                  description = "A Begineer guide programming book",
                  rating =  70)

    

    book3 = Book(id =  "3fa85f64-5717-4562-b3fc-2c963f66afa4",
                  title = "Clean Code",
                  author = "Unknown",
                  description = "A book for Programmers who want to learn how to write clean code",
                  rating =  70)
    

    book4  = Book(id =  "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                  title = "Why",
                  author = "Unknown",
                  description = "A book about knowing your why",
                  rating =  90)
    

    book5  = Book(id =  "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                  title = "Think like a Monk",
                  author = "Unknown",
                  description = "A Book for youths who want to leave independantely ",
                  rating =  99)

    Books.append(book1)
    Books.append(book2)
    Books.append(book3)
    Books.append(book4)
    Books.append(book5)


def http_exception():

    return HTTPException(status_code = 404, detail = "Book not found", headers = {"X-Header_Error":"Nohing to be seen at the UUID"},)