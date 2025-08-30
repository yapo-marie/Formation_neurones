from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import jwt

SECRET_KEY = "YOUR_FAST_API_SECRET_KEY"
ALGORITHM = "HS256"

test_user = {
    "username": "temitope",
    "password": "temipassword",
}

BOOKS = [
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "category": "period drama"},
    {"title": "Great Expectations", "author": "Charles Dickens", "category": "period drama"},
    {"title": "Bourne Identity", "author": "Robert Ludlum", "category": "mystery/thriller"},
    {"title": "Da Vinci Code", "author": "Dan Brown", "category": "mystery/thriller"},
    {"title": "The Match Girl", "author": "Hans Christian Andersen", "category": "tragedy"},
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginItem(BaseModel):
    username: str
    password: str

@app.options("/login")
async def options_login():
    return Response(status_code=200)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
async def user_login(loginitem: LoginItem):
    data = jsonable_encoder(loginitem)
    if data['username'] == test_user['username'] and data['password'] == test_user['password']:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {"token": encoded_jwt}
    return {"message": "login failed"}

@app.get("/books")
async def read_books():
    return BOOKS

@app.post("/books/create_book")
async def create_book(new_book: dict = Body(...)):
    BOOKS.append(new_book)
    return {"message": "Book added"}

@app.put("/books/update_book")
async def update_book(update_book: dict = Body(...)):
    for i, book in enumerate(BOOKS):
        if book['title'].lower() == update_book['title'].lower():
            BOOKS[i] = update_book
            return {"message": "Book updated"}
    return {"error": "Book not found"}

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book['title'].lower() == book_title.lower():
            BOOKS.pop(i)
            return {"message": "Book deleted"}
    return {"error": "Book not found"}
