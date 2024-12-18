from typing import List, Dict

class Book:
    def __init__(self, book_id: int, title: str, author: str, published_year: int):
        self.id = book_id
        self.title = title
        self.author = author
        self.published_year = published_year

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_year': self.published_year
        }


class Member:
    def __init__(self, member_id: int, name: str, email: str, joined_date: str):
        self.id = member_id
        self.name = name
        self.email = email
        self.joined_date = joined_date

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'joined_date': self.joined_date
        }


class InMemoryDatabase:
    def __init__(self):
        self.books: List[Book] = [
            Book(1, "The Great Gatsby", "F. Scott Fitzgerald", 1925),
            Book(2, "1984", "George Orwell", 1949),
            Book(3, "To Kill a Mockingbird", "Harper Lee", 1960),
            Book(4, "Pride and Prejudice", "Jane Austen", 1813),
            Book(5, "Moby-Dick", "Herman Melville", 1851),
        ]

        self.members: List[Member] = [
            Member(1, "Alice Johnson", "alice.johnson@example.com", "2022-01-10"),
            Member(2, "Bob Smith", "bob.smith@example.com", "2022-03-15"),
            Member(3, "Charlie Brown", "charlie.brown@example.com", "2023-05-22"),
            Member(4, "Daisy Miller", "daisy.miller@example.com", "2023-08-01"),
            Member(5, "Ethan Hunt", "ethan.hunt@example.com", "2024-02-14"),
        ]

    def add_book(self, book: Book):
        self.books.append(book)

    def get_books(self) -> List[Book]:
        return self.books

    def find_book_by_id(self, book_id: int) -> Book:
        return next((book for book in self.books if book.id == book_id), None)

    def delete_book(self, book_id: int):
        self.books = [book for book in self.books if book.id != book_id]

    def add_member(self, member: Member):
        self.members.append(member)

    def get_members(self) -> List[Member]:
        return self.members

    def find_member_by_id(self, member_id: int) -> Member:
        return next((member for member in self.members if member.id == member_id), None)

    def delete_member(self, member_id: int):
        self.members = [member for member in self.members if member.id != member_id]
