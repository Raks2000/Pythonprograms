# Program to print right-angled triangle pattern
n = 5  # number of rows

for i in range(n):
    for j in range(i + 1):
        print("*", end=" ")
    print()