#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
// Define variables ChangeOwed (what change is owed), Balance (change when converted to cents) and CoinCounter (keeps track of number of coins used)
    float ChangeOwed;
    int Balance;
    int CoinCounter = 0;

// Prompt user to input amount of changed owed, repeat until appropriate value given
    do
    {
        ChangeOwed = get_float("Change owed: \n");

    }
    while (ChangeOwed <= 0);

// Round value and convert from dollar to cents

    Balance = round(ChangeOwed * 100);

// Check if balance is greater than or equal to 25, subtract balance by 25, increase coin counter by 1

    while (Balance >= 25)
    {
        Balance = Balance - 25;
        CoinCounter++;
    }
// Check if balance is greater than or equal to 10, subtract balance by 10, increase coin counter by 1
    while (Balance >= 10)
    {
        Balance = Balance - 10;
        CoinCounter++;
    }
// Check if balance is greater than or equal to 5, subtract balance by 5, increase coin counter by 1
    while (Balance >= 5)
    {
        Balance = Balance - 5;
        CoinCounter++;
    }
// Check if balance is greater than or equal to 1, subtract balance by 1, increase coin counter by 1
    while (Balance >= 1)
    {
        Balance = Balance - 1;
        CoinCounter++;
    }
// Print total CoinCounter value (the number of coins needed for change)
    printf("Number of coins needed %d\n", CoinCounter);


}
