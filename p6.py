def is_prime(number):
    # Numbers less than 2 are not prime
    if number < 2:
        return False
    
    # Check for divisibility from 2 to square root of number
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    
    return True

# Get input from user
num = int(input("Enter a number to check if it's prime: "))

# Check and display result
if is_prime(num):
    print(f"{num} is a prime number")
else:
    print(f"{num} is not a prime number")