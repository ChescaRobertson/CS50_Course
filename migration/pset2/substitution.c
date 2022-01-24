#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>



int main(int argc, string argv[])
{
// Validate key, check if entered a key on command line, prompt for this if not

    if (argc != 2)
    {
        printf("Usage: ./substitution Key\n");
        return 1;
    }

// Check key only has 26 characters

    int keylength = strlen(argv[1]);
    if (keylength != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

// Check key contains only letters

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isalpha(argv[1] [i]))
        {
            printf("Key must only contain letters\n");
            return 1;
        }
    }

//Check letters are not repeated


    int count = 0;

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        count = 1;
        for (int j = i + 1; j < strlen(argv[1]); j++)
        {
            if (argv[1][i] == argv[1][j] && argv[1][i] != ' ')
            {
                count++;
                argv[1][j] = '0';
            }
        }
        if (count > 1 && argv[1][i] != '0')
        {
            printf("Key must not contain repeated characters\n");
            return 1;
        }
    }


// Get User input

    string s = get_string("Plaintext: ");

// Find difference between plaintext character and key character in ASCII number, store this in variable difference

    string difference = argv[1];
    for (int i = 'A'; i <= 'Z'; i++)
    {
        difference[i - 'A'] = toupper(difference[i - 'A']) - i;
    }

// Print cihpertext and converted text

    printf("ciphertext: ");

// Encrypt plaintext to ciphertext by subtracting difference and comparing to index number in key

    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (isalpha(s[i]))
        {
            s[i] = s[i] + difference[s[i] - (isupper(s[i]) ? 'A' : 'a')];
            printf("%c", s[i]);
        }
        else
        {
            s[i] = s[i];
            printf("%c", s[i]);
        }

    }
    printf("\n");
    return 0;
}
