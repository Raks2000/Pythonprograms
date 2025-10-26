import random

# Number Guessing Game

secret = random.randint(1, 10)
#print(secret)
guess = int(input("Guess a number between 1 and 10: "))

while guess != secret:
    if guess < secret:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
    guess = int(input("Guess again: "))

print("🎉 Correct! The number was", secret)
