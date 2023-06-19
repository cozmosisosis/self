import csv
"""docstring"""
def main():
    """description"""
    csvfile = open("excel.csv", newline= '')
    file = csv.DictReader(csvfile )
    for row in file:
        print(f"{row['name']} {row['score']}" )
    csvfile = open("excel.csv", "a")
    file = csv.writer(csvfile)
    new_name = input("New name: ")
    new_score = input("New score: ")
    file.writerow([new_name,new_score])


main()