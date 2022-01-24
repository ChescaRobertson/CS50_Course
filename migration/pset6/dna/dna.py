import csv
from sys import argv, exit


def get_maximum_num_of_times_substring(s, sub):
    # Calculate the maximum number of times a substring is repeated
    # s:   [ATATATTATAT]
    # ans: [00000000000] # starting at that index how many times des the subsrting sub repeat in s
    # sub: AT
    
    # iterate backwards over string in groups of length substring, how many times does it repeat? Fill array with this answer, return the maximum answer
    ans = [0] * len(s)
    for i in range(len(s) - len(sub), -1, -1):
        if s[i: i + len(sub)] == sub:
            if i + len(sub) > len(s) - 1:
                ans[i] = 1
            else:
                ans[i] = 1 + ans[i + len(sub)]
    return max(ans)
    
    
def print_match(reader, actual):
    # Checks for matches in repeats of subdstrings with csv file and returns either name or no match
    for line in reader:
        person = line[0]  # Extract person name from line
        values = [int(val) for val in line[1:]]  # takes each number from the csv file for each name and stores in values array
        if values == actual:
            print(person)
            return
    print("No match")
    
            
def main():
    # Check for correct command line input
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()
    
    # Open and read csv file
    with open(argv[1]) as csv_file:
        reader = csv.reader(csv_file)
        # takes the DNA substrings from the first line of csv and stores in array all_sequences
        all_sequences = next(reader)[1:]
            
        # Open and read text file
        with open(argv[2], 'r') as txt_file:
            s = txt_file.read()
            # Call function to get maximum number of substrings in the sequence as provided from the csv file
            actual = [get_maximum_num_of_times_substring(s, seq) for seq in all_sequences]
           
        # Iterate over csv file and find person who matches the 'actual' answer from the function
        print_match(reader, actual)


if __name__ == "__main__":
    main()