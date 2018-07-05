from nltk.metrics import edit_distance
import os
import sys

"""
TODO: implement levenshtein
"""
def printtest(matrix, m, n):
    for i in range(m):
        for j in range(n):
            print '\t',matrix[i][j],
        print ''

def levenshtein(str1, str2):
    # Using NLTK's edit_distance to test result
    #sm = edit_distance(str1, str2, substitution_cost=2)
    #print sm,

    m = len(str1)
    n = len(str2)
    # Initialize matrix
    matrix = [[0 for x in range(n+1)] for y in range(m+1)]

    # Set PREFIXES
    for i in range(m+1):
        matrix[i][0] = i
    for j in range(n+1):
        matrix[0][j] = j

    for j in range(n):
        for i in range(m):
            if str1[i] == str2[j]:
                cost = 0
            else:
                cost = 2
            matrix[i+1][j+1] = min(matrix[i][j+1] + 1, matrix[i+1][j] + 1, matrix[i][j] + cost)
    return matrix[m][n]

"""
You should not need to edit this function.
"""
def process_dir(data_path):
    # get candidates
    lst_input = []
    for filename in os.listdir(data_path):
        if filename.endswith('.txt'):
            lst_input.append(filename)
    return lst_input

"""
You should not need to edit this function.
"""
def main(data_path, gold_path):
    lst_input = process_dir(data_path)
    match = 0
    lev_gold = {}
    with open(os.path.join(gold_path, 'gold'), 'r') as fg:
        for line in fg:
            file, lev_g = line.replace('\n', '').split(' ')
            lev_gold.setdefault(file, lev_g)
    for file in lst_input:
        with open(os.path.join(data_path,file), 'r') as f:
            lines = f.readlines()
            str1, str2 = lines[0].split('\n')[0], lines[1].split('\n')[0]
            #guess levenshtein
            lev = levenshtein(str1, str2)
            #nltk levenshtein
            #lev_gold = levenshtein1(str1, str2)
            print file,' Your levenshtein:', lev, ' levenshtein:', lev_gold[file]
            if lev==int(lev_gold[file]): match += 1
    print 'Total match = ', match

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tlevenshtein.py <data_dir> <gold_dir>'
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
