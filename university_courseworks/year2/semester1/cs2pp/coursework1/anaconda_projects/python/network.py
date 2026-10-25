"""
def file_to_edge_list(file_path):
    import csv

    with open('./data/citations.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            print(row)

if __name__ == "__main__":
    print(file_to_edge_list(file_path))
"""

import csv

with open('university_courseworks/year2/semester1/cs2pp/coursework1/data/citations.tsv') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        print(row)

