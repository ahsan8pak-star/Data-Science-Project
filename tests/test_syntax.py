# Test cases for syntax fundamentals
def test_addition():
    assert 1 + 1 == 2

def test_divide():
    assert 4 / 2 == 2

def test_prime_check():
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    assert is_prime(2) == True
    assert is_prime(7) == True
    assert is_prime(1) == False

def test_string_methods():
    assert "hello".upper() == "HELLO"
    assert "apple".startswith("a")
    assert "world".endswith("d")

def test_list_methods():
    fruits = ["apple"]
    fruits.append("banana")
    assert len(fruits) == 2
    assert "banana" in fruits

def test_function_definitions():
    def greet(name):
        return f"Hello, {name}!"
    assert greet("Aiman") == "Hello, Aiman!"
