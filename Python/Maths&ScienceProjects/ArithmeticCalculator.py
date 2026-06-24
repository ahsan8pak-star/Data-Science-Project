def arithmetic (num1, op, num2):
    
    match op:
    
        case "+":
            return num1 + num2
    
        case "-":
            return num1 - num2
    
        case "*":
            return num1 * num2
    
        case "/":

            if num2 == 0:
                print("Undefined. You can't divide anything by 0.")
    
            else:
                return num1 / num2 
    
        case "//":
    
            if num2 == 0:
                print("Undefined. You can't divide anything by 0.")
    
            else:
                return num1 // num2
    
        case "%":
    
            if num2 == 0:
                print("Undefined. You can't divide anything by 0.")
    
            else:
                return num1 % num2 
            
try:
    print("=======================")
    print(" ARITHMETIC CALCULATOR ")        
    print("=======================")
    print("")
    print("<================>")
    print("<  MENU   GUIDE  >")
    print("<================>")
    print("")
    print(" ____________________________________________________")
    print("/                                                    \ ")
    print("| 1) + = addition         4) / = division            |")
    print("| 2) - = subtraction      5) // = base / quotient    |") 
    print("| 3) * = multiplication   6) % = remainder / modulus |")
    print("\                                                    /")
    print(" ````````````````````````````````````````````````````")
    print("")

    num1 = float(input("Enter the 1st number: ").strip())
    op = input("Enter the operation: ").strip()
    num2 = float(input("Enter the 2nd number: ").strip())

    result = arithmetic(num1, op, num2)

    print("----------------")
    print(f"| Result: {result}  |")
    print("----------------")

except ValueError:
    print("Incorrect Format.")

