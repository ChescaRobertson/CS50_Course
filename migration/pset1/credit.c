# include <stdio.h>
# include <cs50.h>
# include <math.h>

int main (void)
{

// Defines long variable credit card number (ccNumber)
long long ccNumber;

// Prompt for user input, repeat if positive integer not given
do
{
    ccNumber = get_long("Number: ");
} while (ccNumber < 0);

// Define long digitvalidation (this is equal to ccNumber but can be manipulated to allow calculation of integer length) and int digitcount (used to count integer length). Print invalid if digitcount is not 13, 15 or 16
long long digitvalidation = ccNumber;
int digitcount = 0;

while (digitvalidation > 0)
{
    digitvalidation = (digitvalidation / 10);
    digitcount++;
}
if (digitcount != 13 && digitcount != 15 && digitcount != 16)
{
    printf("INVALID\n");
}
else {

//Multiplies every other digit by 2 starting from second last number

int digit1 = (ccNumber/10 % 10) * 2;
int digit2 = (ccNumber/1000 % 10) * 2;
int digit3 = (ccNumber/100000 % 10) * 2;
int digit4 = (ccNumber/10000000 % 10) * 2;
int digit5 = (ccNumber/1000000000 % 10) * 2;
int digit6 = (ccNumber/100000000000 % 10) * 2;
int digit7 = (ccNumber/10000000000000 % 10) * 2;
int digit8 = (ccNumber/1000000000000000 % 10) * 2;

//Splits these products into digits e.g. 14 = 1 + 4 and culmulatively sum
int digitsum = (digit1 % 10) + (digit1/10 % 10);
digitsum = (digitsum + (digit2 % 10) + (digit2 / 10));
digitsum = (digitsum + (digit3 % 10) + (digit3 / 10));
digitsum = (digitsum + (digit4 % 10) + (digit4 / 10));
digitsum = (digitsum + (digit5 % 10) + (digit5 / 10));
digitsum = (digitsum + (digit6 % 10) + (digit6 / 10));
digitsum = (digitsum + (digit7 % 10) + (digit7 / 10));
digitsum = (digitsum + (digit8 % 10) + (digit8 / 10));

//Finds the remaining digits in the ccNumber
int digit9 = (ccNumber % 10);
int digit10 = (ccNumber/100 % 10);
int digit11 = (ccNumber/10000 % 10);
int digit12 = (ccNumber/1000000 % 10);
int digit13 = (ccNumber/100000000 % 10);
int digit14 = (ccNumber/10000000000 % 10);
int digit15 = (ccNumber/1000000000000 % 10);
int digit16 = (ccNumber/100000000000000 % 10);

//Adds the sum of remaining digits to the sum of digits multiplied by 2
digitsum = digitsum + digit9 + digit10 + digit11 + digit12 + digit13 + digit14 + digit15 + digit16;

//Checks if digitsum gives a valid credit card number (ends in 0)
if ((digitsum % 10) != 0)
    {
        printf("INVALID\n");
    }
else
{

//Validation for American Express
long long amex = (ccNumber / 10000000000000);
if (digitcount == 15)
{
    if (amex != 34 && amex != 37)
    {
        printf("INVALID\n");
    } else
    {
        printf("AMEX\n");
    }
}

//First validation for Visa
long long visa13 = (ccNumber / 1000000000000);
if (digitcount == 13)
{
    if (visa13 != 4)
    {
        printf("INVALID\n");
    } else
    {
        printf("VISA\n");
    }
}

//Second validation for Visa and validation for Mastercard
long long visa16 = (ccNumber/1000000000000000);
long long mastercard = (ccNumber / 100000000000000);
if (digitcount == 16)
{
    if(visa16 == 4)
    {
        printf("VISA\n");
    }
   else if (mastercard != 51 && mastercard != 52 && mastercard != 53 && mastercard != 54 && mastercard !=55)
   {
       printf("INVALID\n");
   }
   else
   {
       printf("MASTERCARD\n");
   }
}
}
}
}
