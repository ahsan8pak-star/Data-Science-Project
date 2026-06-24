def celsius(f):

    c = 5/9 * (f - 32) 
    return c

def fahrenheit(f):
    
    c = round(celsius(f), 2)
    print(f, "degrees Fahrenheit is", c, "degrees Celsius")

def CELCIUS(c):
    
    f = (9/5 * c) + 32 
    return f

def FAHRENHEIT(c):
    
    f = round(CELCIUS(c), 2) 
    print(c, "degrees Celsius is", f, "degrees Fahrenheit")

try:

    i = input("Celsius or Fahrenheit (C/F): ").strip()
    
    if i and i[0].upper() == "F":
    
        f = float(input("Enter Fahrenheit: "))
        fahrenheit(f)
    
    else:
    
        c = float(input("Enter Celsius: "))
        FAHRENHEIT(c)

except ValueError:

    print("Numbers only!")

