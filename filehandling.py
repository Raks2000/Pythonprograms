#program 1: 
with open("example.txt", "wb") as f:
    f.write("Hello\n".encode("utf-8"))

with open("example.txt", "a") as f:       # text append mode
    f.write("World\n")

with open("example.txt", "rb") as f:
    print(f.read())


#program 2:
from collections import Counter

with open("example1.txt", "r") as f:
    words = f.read().split()

count = Counter(words)
for word, freq in count.items():
    print(f"{word}: {freq}")

#program 3:


with open("example1.txt", "r") as f:
    lines = f.readlines()

with open("no_blank.txt", "w") as f:
    for line in lines:
        if line.strip():  # only write non-empty lines
            f.write(line)

print("Blank lines removed successfully!")


#program 4:
with open("example1.txt", "r") as f:
    content = f.read()

with open("reversed.txt", "w") as f:
    f.write(content[::-1])

print("File content reversed successfully!")


