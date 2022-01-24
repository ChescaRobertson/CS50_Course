import csv
from sys import argv, exit
from cs50 import SQL

# Check for correct command line input
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)   

# Connect to database    
db = SQL("sqlite:///students.db")

# Open and read csv file
with open(argv[1]) as characters:
    reader = csv.DictReader(characters, delimiter=",")

# Input data from each row in csv file    
    for row in reader:
        house = row["house"]
        birth = row["birth"]
        names = row["name"]
        name_list = names.split()
        
        # Set first name equal to first name in list, check for middle name, setting to None if not present
        firstname = name_list[0]
        if len(name_list) == 2:
            middle = None
            lastname = name_list[1]
            # Excute SQL query to insert names into database for those with no middle name
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       firstname, None, lastname, house, birth)
        else:
            middle = name_list[1]
            lastname = name_list[2]
            # Excute SQL query to insert names into database for those with middle names
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       firstname, middle, lastname, house, birth)