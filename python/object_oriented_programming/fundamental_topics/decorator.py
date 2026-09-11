# Decorator = A function that extends the behavior of another function
# Without modifying the base function
# Pass the base function as an argument to the decorator

def add_sprinkles(func):
    def wrapper(*args, **kwargs):
        print("*You added sprinkles.*")
        func(*args, **kwargs)
    return wrapper

def add_fudge(func):
    def wrapper(*args, **kwargs):
        print("*You added fudge.*")
        func(*args, **kwargs)
    return wrapper

def add_flake(func):
    def wrapper(*args, **kwargs):
        print("*You added a flake.*")
        func(*args, **kwargs)
    return wrapper

@add_sprinkles # def add_sprinkles(func) -> line 5
@add_fudge # def add_fudge(func) -> line 11
@add_flake # def add_flake(func) -> line 17
def get_ice_cream(flavour):
    print(f"Here is your {flavour} ice cream.")

get_ice_cream("vanilla")
get_ice_cream("chocolate")
get_ice_cream("strawberry")

