#include "helpers.h"
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
//Iterate over height
    for (int i = 0; i < height; i++)
    {

        //Iterate through width
        for (int j = 0; j < width; j++)
        {
            // Define red, green and blue integers (for ease of understanding)
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // Find average of red, green and blue colour number to nearest whole integer
            int avg = round(((float)red + (float)green + (float)blue) / 3);

            // Set each pixel red, green, blue values to average
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;

        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //Iterate over height
    for (int i = 0; i < height; i++)
    {

        //Iterate through width
        for (int j = 0; j < width; j++)
        {
            // Define red, green and blue integers (for ease of understanding)
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // Calculate sepia values for each pixel
            int sepiaRed = round(.393 * (float)red + .769 * (float)green + .189 * (float)blue);
            int sepiaGreen =  round(.349 * (float)red + .686 * (float)green + .168 * (float)blue);
            int sepiaBlue =  round(.272 * (float)red + .534 * (float)green + .131 * (float)blue);

            // Check if sepiaRed is within range, set red to sepiaRed, set to 255 if out of range
            if (sepiaRed < 256)
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            else
            {
                image[i][j].rgbtRed = 255;
            }

            // Check if sepiaGreen is within range, set green to sepiaGreen, set to 255 if out of range
            if (sepiaGreen < 256)
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
            else
            {
                image[i][j].rgbtGreen = 255;
            }

            // Check if sepiaBlue is within range, set blue to sepiaBlue, set to 255 if out of range
            if (sepiaBlue < 256)
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
            else
            {
                image[i][j].rgbtBlue = 255;
            }

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare int m, half of width of row
    int m = round((float)width / 2);

    // Iterature through height
    for (int i = 0; i < height; i++)
    {

        // Iterate through half width
        for (int j = 0; j < m; j++)
        {
            // Swap left hand wth right-hand values in row using a temporary variable
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE newImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newImage[i][j] = image[i][j];
        }
    }

    for (int i = 0, red, green, blue, counter; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = green = blue = counter = 0;
            // add the center pixel
            if (i >= 0 && j >= 0)
            {
                red += newImage[i][j].rgbtRed;
                green += newImage[i][j].rgbtGreen;
                blue += newImage[i][j].rgbtBlue;
                counter++;
            }
            // add below pixel
            if (i >= 0 && j - 1 >= 0)
            {
                red += newImage[i][j - 1].rgbtRed;
                green += newImage[i][j - 1].rgbtGreen;
                blue += newImage[i][j - 1].rgbtBlue;
                counter++;
            }
            // add right pixel
            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                red += newImage[i][j + 1].rgbtRed;
                green += newImage[i][j + 1].rgbtGreen;
                blue += newImage[i][j + 1].rgbtBlue;
                counter++;
            }
            // add left pixel
            if (i - 1 >= 0 && j >= 0)
            {
                red += newImage[i - 1][j].rgbtRed;
                green += newImage[i - 1][j].rgbtGreen;
                blue += newImage[i - 1][j].rgbtBlue;
                counter++;
            }
            // add left below pixel
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += newImage[i - 1][j - 1].rgbtRed;
                green += newImage[i - 1][j - 1].rgbtGreen;
                blue += newImage[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            // add left upper pixel
            if ((i - 1 >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                red += newImage[i - 1][j + 1].rgbtRed;
                green += newImage[i - 1][j + 1].rgbtGreen;
                blue += newImage[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            // add upper pixel
            if ((i + 1 >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                red += newImage[i + 1][j].rgbtRed;
                green += newImage[i + 1][j].rgbtGreen;
                blue += newImage[i + 1][j].rgbtBlue;
                counter++;
            }
            // add below right pixel
            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                red += newImage[i + 1][j - 1].rgbtRed;
                green += newImage[i + 1][j - 1].rgbtGreen;
                blue += newImage[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            // add upper right pixel
            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                red += newImage[i + 1][j + 1].rgbtRed;
                green += newImage[i + 1][j + 1].rgbtGreen;
                blue += newImage[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
        }
    }

    return;
}