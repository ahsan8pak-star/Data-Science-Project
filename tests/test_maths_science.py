# Test cases for math, calculators, and converters
def test_arithmetic_calculator():
    # Basic arithmetic operations
    assert 2 + 3 == 5
    assert 10 - 4 == 6
    assert 3 * 4 == 12
    assert 20 / 4 == 5

def test_celsius_to_fahrenheit():
    # Example conversion: 0°C = 32°F
    celsius = 0
    fahrenheit = (celsius * 9/5) + 32
    assert fahrenheit == 32
    
    # 100°C = 212°F
    celsius = 100
    fahrenheit = (celsius * 9/5) + 32
    assert fahrenheit == 212

def test_weight_converter():
    # Example: 1kg = 2.20462 lbs
    kg = 1
    lbs = round(kg * 2.20462, 2)
    assert lbs == 2.20
    
    # 5kg conversion
    kg = 5
    lbs = round(kg * 2.20462, 2)
    assert lbs == 11.02

def test_time_converter():
    # 1 hour = 60 minutes
    hours = 1
    minutes = hours * 60
    assert minutes == 60
    
    # 2 hours = 120 minutes
    hours = 2
    minutes = hours * 60
    assert minutes == 120

def test_geometry_area():
    # Circle area: π * r²
    import math
    radius = 5
    area = round(math.pi * (radius ** 2), 2)
    assert area == 78.54

def test_geometry_perimeter():
    # Rectangle perimeter: 2(l + w)
    length = 10
    width = 5
    perimeter = 2 * (length + width)
    assert perimeter == 30

def test_geometry_volume():
    # Cube volume: s³
    side = 3
    volume = side ** 3
    assert volume == 27
    
    # Sphere volume: (4/3) * π * r³
    import math
    radius = 2
    volume = round((4/3) * math.pi * (radius ** 3), 2)
    assert volume == 33.51
