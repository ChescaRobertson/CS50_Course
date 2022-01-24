import math
from cs50 import get_string

# Declare variables, letters (number of letters), words (number of words) and sentences (number of sentences)
letters = 0
words = 1
sentences = 0

# Prompt user to input text
text = get_string("Text: ")
# Declare variable n (total string length)
n = len(text)

# Loop to count total number of letters
for i in range(n):
    if text[i].isalpha() == True:
        letters += 1

# Loop to count total number of words
for i in range(n):
    if text[i].isspace() == True:
        words += 1

# Loop to count total number of sentences
for i in range(n):
    if (text[i] == '.' or text[i] == '?' or text[i] == '!'):
        sentences += 1

# Calculate average number of letters per 100 words (L)
L = (letters / words) * 100

# Calculate average number of words per 100 sentences (S)
S = (sentences / words) * 100

# Calculate Reading Grade using Coleman-Liau index formula
index = 0.0588 * L - 0.296 * S - 15.8
ReadingGrade = round(index)

# Print result
if (ReadingGrade > 16):
    print("Grade 16+")
elif (ReadingGrade < 1):
    print("Before Grade 1")
else:
    print("Grade " + str(ReadingGrade))
