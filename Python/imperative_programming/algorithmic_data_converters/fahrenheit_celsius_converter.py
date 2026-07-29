def fahrenheit_to_celcius(f):

    c = 5/9 * (f - 32) 
    return c

def format_celcius(f):
    
    c = fahrenheit_to_celcius(f)
    print(f"{f:.1f} degrees Fahrenheit is {c:.1f} degrees Celsius")

def celcius_to_fahrenheit(c):
    
    f = (9/5 * c) + 32 
    return f

def format_fahrenheit(c):
    
    f = celcius_to_fahrenheit(c)
    print(f"{c:.1f} degrees Celsius is {f:.1f} degrees Fahrenheit")

try:

    i = input("Celsius or Fahrenheit (C/F): ").strip()
    
    if i and i[0].upper() == "F":
    
        f = float(input("Enter Fahrenheit: "))
        format_celcius(f)
    
    else:
    
        c = float(input("Enter Celsius: "))
        format_fahrenheit(c)

except ValueError:

    print("Numbers only!")

