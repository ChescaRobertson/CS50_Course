from cs50 import get_int

# receives input for user, repeats until integer between 1 and 8 given
while True:
    n = get_int("Height: ")
    if 0 < n < 9:
        break

# nested for loops to create a pyramid of height n
for i in range(n):
    for j in range(n - i - 1):
        print(" ", end="")

    for k in range(i + 1):
        print("#", end="")
    print("  ", end="")

    for l in range(i + 1):
        print("#", end="")
    print()
