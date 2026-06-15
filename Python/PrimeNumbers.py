def is_prime(n):
    
    # Assume the number is prime and tries to find other numbers which aren't i.e. counter examples
    flag = True

    # Deals with special cases i.e. only these unique numbers in this scenario
    if n == 0 or n == 1:
        flag = False
    
    # Loop through all numbers between 2 and n - 1, and check if n is NOT prime
    i = 2
    while i < n:
        if n % i == 0:
            flag = False
        i = i + 1
    
    # Output the current value of flag
    return flag