import typer
import requests
import json

app = typer.Typer()
API_URL = "http://127.0.0.1:8000"

@app.command()
def create_book(title: str, author: str, year: int):
    payload = {"title": title, "author": author, "year": year}
    response = requests.post(f"{API_URL}/books/", json=payload)
    typer.echo(json.dumps(response.json(), indent=2))

@app.command()
def get_books():
    response = requests.get(f"{API_URL}/books/")
    typer.echo(json.dumps(response.json(), indent=2))

@app.command()
def get_book(book_id: int):
    response = requests.get(f"{API_URL}/books/{book_id}")
    typer.echo(json.dumps(response.json(), indent=2))

@app.command()
def update_book(book_id: int, title: str, author: str, year: int):
    payload = {"title": title, "author": author, "year": year}
    response = requests.put(f"{API_URL}/books/{book_id}", json=payload)
    typer.echo(json.dumps(response.json(), indent=2))

@app.command()
def delete_book(book_id: int):
    response = requests.delete(f"{API_URL}/books/{book_id}")
    typer.echo(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    app()