from cs50 import get_int 
import math

        
# Prompt for user input, repeat if positive integer not given
while True:
    ccNumber = get_int("Number: ")
    if ccNumber > 0:
        break
    
# Check number length for validation    
x = len(str(ccNumber))
 
if(x != 13 and x != 15 and x != 16):
    print("INVALID")
else:
     
    digit1 = math.floor(math.floor(ccNumber/10 % 10) * 2)
    digit2 = math.floor(math.floor(ccNumber/1000 % 10) * 2)
    digit3 = math.floor(math.floor(ccNumber/100000 % 10) * 2)
    digit4 = math.floor(math.floor(ccNumber/10000000 % 10) * 2)
    digit5 = math.floor(math.floor(ccNumber/1000000000 % 10) * 2)
    digit6 = math.floor(math.floor(ccNumber/100000000000 % 10) * 2)
    digit7 = math.floor(math.floor(ccNumber/10000000000000 % 10) * 2)
    digit8 = math.floor(math.floor(ccNumber/1000000000000000 % 10) * 2)
    
    # Splits these products into digits e.g. 14 = 1 + 4 and culmulatively sum
    digitsum = math.floor(digit1 % 10) + math.floor(digit1/10 % 10)
    digitsum = (digitsum + math.floor(digit2 % 10) + math.floor(digit2 / 10))
    digitsum = (digitsum + math.floor(digit3 % 10) + math.floor(digit3 / 10))
    digitsum = (digitsum + math.floor(digit4 % 10) + math.floor(digit4 / 10))
    digitsum = (digitsum + math.floor(digit5 % 10) + math.floor(digit5 / 10))
    digitsum = (digitsum + math.floor(digit6 % 10) + math.floor(digit6 / 10))
    digitsum = (digitsum + math.floor(digit7 % 10) + math.floor(digit7 / 10))
    digitsum = (digitsum + math.floor(digit8 % 10) + math.floor(digit8 / 10))
    
    # Finds the remaining digits in the ccNumber
    digit9 = math.floor((ccNumber % 10))
    digit10 = math.floor(math.floor(ccNumber/100) % 10)
    digit11 = math.floor(math.floor(ccNumber/10000) % 10)
    digit12 = math.floor(math.floor(ccNumber/1000000) % 10)
    digit13 = math.floor(math.floor(ccNumber/100000000) % 10)
    digit14 = math.floor(math.floor(ccNumber/10000000000) % 10)
    digit15 = math.floor(math.floor(ccNumber/1000000000000) % 10)
    digit16 = math.floor(math.floor(ccNumber/100000000000000) % 10)
    
    # Adds the sum of remaining digits to the sum of digits multiplied by 2
    digitsum = digitsum + digit9 + digit10 + digit11 + digit12 + digit13 + digit14 + digit15 + digit16
    
    # Checks if digitsum gives a valid credit card number (ends in 0)
    if ((digitsum % 10) != 0):
        print("INVALID")
    else:
    
        # Validation for American Express
        amex = math.floor(ccNumber / 10000000000000)
        if (x == 15):
            if (amex != 34 and amex != 37):
                print("INVALID")
            else:
                print("AMEX")
        
        # First validation for Visa
        visa13 = math.floor(ccNumber / 1000000000000)
        if (x == 13):
            if (visa13 != 4):
                print("INVALID VISA")
            else:
                print("VISA")
        
        # Second validation for Visa and validation for Mastercard
        visa16 = math.floor(ccNumber/1000000000000000)
        mastercard = math.floor(ccNumber / 100000000000000)
        if (x == 16):
            if(visa16 == 4):
                print("VISA")
            elif (mastercard != 51 and mastercard != 52 and mastercard != 53 and mastercard != 54 and mastercard != 55):
                print("INVALID")
            else:
                print("MASTERCARD")
        