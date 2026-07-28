# Aggregation = Represents a relationship where 1 Object (Whole)
# Contains refrences at least 1 Independent Objects (parts)

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def list_book(self):
        return [f"{book.title} by {book.author}" for book in self.books] # for loop to collect every 'book' recalled in 'self.books'

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

library = Library("London Museum Library")

book1 = Book("Alex Rider: Stormbreaker", "Anthony Horowitz")
book2 = Book("Harry Potter: The Philosopher Stone", "J.K Rowling")
book3 = Book("The Great Gatsby", "F.Scott Fitzegerald")
book4 = Book("The Hobbit", "J.R.R Tolkein")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)

print(library.name)
print("-" * 21) # Line Seperator for Library name and its books below

for book in library.list_book():
    print(book)

