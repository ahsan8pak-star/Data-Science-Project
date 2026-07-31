# Magic methods = Dunder methods (double underscore -> __) __init__, __str__, __eq__
# Automatically called by many Python's built-in operations.
# Allows Developers to define or customise the object's behaviour
# Refer to nested_classes.py on lines 38-39 for context

class Book:

    def __init__(self, title, author, num_pages):
        self.title = title
        self.author = author
        self.num_pages = num_pages

    def __str__(self): # (str)ing
        return f"'{self.title}' by {self.author}"

    def __eq__(self, other): # (eq)uivilant
        return self.title == other.title and self.author == other.author

    def __lt__(self, other): # (l)ess (t)han
        return self.num_pages < other.num_pages

    def __gt__(self, other): # (g)reater (t)han
        return self.num_pages > other.num_pages

    def __add__(self, other): # (add)ition
        return f"{self.num_pages + other.num_pages} pages"

    def __contains__(self, keyword): # (contain)er(s)
        return keyword in self.title or keyword in self.author

    def __getitem__(self, key): # (get) (item) 
        if key == "title":
            return self.title
        elif key == "author":
            return self.author
        elif key == "num_pages":
            return self.num_pages
        else:
            return f"Key '{key}' was not found"

book1 = Book("The Hobbit", "J.R.R. Tolkien", 310)
book2 = Book("Harry Potter and The Philosopher's Stone", "J.K. Rowling", 223)
book3 = Book("The Lion, the Witch and the Wardrobe", "C.S. Lewis", 172)

print(book1) # __str__
print(book1 == book3) # __eq__
print(book1 < book2) # ___lt__
print(book2 > book3) # __gt__
print(book1 + book2) # __add__
print("Lion" in book3) # __contains__
print(book3['title']) # __getitem__