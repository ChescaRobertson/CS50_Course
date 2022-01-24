import sys
from cs50 import SQL

# Check for correct command line input
if len(sys.argv) != 2:
    print("Usage: python roster.py house")
    exit(1)
    
# Connect to database 
db = SQL("sqlite:///students.db")

# Establish which house the query is related to
house = sys.argv[1]

# Run SQL query creating a results table for the apporpriate house
results = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last ASC, first ASC", house)

# Check for middle names in results, if set to None, do not print middle name
for row in results:
    if row["middle"] != None:
        print(f'{row["first"]} {row["middle"]} {row["last"]}, born {row["birth"]}')
    else:
        print(f'{row["first"]} {row["last"]}, born {row["birth"]}')