#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
// Declare variables, letters (number of letters), words (number of words) and sentences (number of sentences)
    int letters = 0;
    int words = 1;
    int sentences = 0;

// Prompt user to input text

    string text = get_string("Text: ");

// Declare variable n (total string length)
    int n = strlen(text);

// Loop to count total number of letters
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }


// Loop to count total number of words
    for (int i = 0; i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }


// Loop to count total number of sentences
    for (int i = 0; i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }


// Calculate average number of letters per 100 words (L)

    float L = 0;

    L = ((float)letters / (float)words) * 100;

// Calculate average number of words per 100 sentences (S)

    float S = 0;

    S = ((float)sentences / (float)words) * 100;

// Calculate Reading Grade using Coleman-Liau index formula

    float index = 0;
    index = 0.0588 * L - 0.296 * S - 15.8;
    int ReadingGrade = round(index);

// Print result

    if (ReadingGrade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (ReadingGrade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", ReadingGrade);
    }

}
