#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // 1. Get the height from the user (must be between 1 and 8)
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // 2. Loop for the rows
    for (int row = 0; row < height; row++)
    {
        // 3. Loop for printing spaces
        for (int space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }

        // 4. Loop for printing hashes
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Move to the next line after finishing the row
        printf("\n");
    }
}
