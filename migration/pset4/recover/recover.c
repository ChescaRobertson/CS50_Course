#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

typedef uint8_t BYTE;

#define BLOCK_SIZE 512
#define FILE_NAME_SIZE 8



bool is_start_new_jpg(BYTE buffer[]);

int main(int argc, char *argv[])
{
    
    //Check for valid usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1; 
    }
    
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("File not found\n");
        return 1;
    }
    
    // Set up integer file_index to keep track of amount of jpgs
    BYTE buffer[BLOCK_SIZE];
    int file_index = 0;
    // Create boolean to test if firts jpeg found, set to false
    bool have_found_first_jpg = false;
    // open an output file to write into
    FILE *outfile;
    // read infile a 512 block at a time, if header recognised asstart of new jpg check if first found, if not close current jpeg first
    while (fread(buffer, BLOCK_SIZE, 1, infile))
    {
        if (is_start_new_jpg(buffer))
        {
            if (!have_found_first_jpg)
            {
                have_found_first_jpg = true;
            } 
            else
            {
                fclose(outfile);
            }
             
              
            //Create a new filename for new jpeg and write into it
            char filename[FILE_NAME_SIZE];
            sprintf(filename, "%03i.jpg", file_index++);
            outfile = fopen(filename, "w");
            if (outfile == NULL)
            {
                return 1; 
            }
            
            fwrite(buffer, BLOCK_SIZE, 1, outfile);
              
        }
        // if not new jpeg and already found first keep writing into file
        else if (have_found_first_jpg)
        {
            // keep writing the previous file
            fwrite(buffer, BLOCK_SIZE, 1, outfile);
        }
        
    }
    //close both files
    fclose(outfile);
    fclose(infile);
    
}    

// boolean method to check if header is jpeg header
bool is_start_new_jpg(BYTE buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
    
}
    
  
 
 