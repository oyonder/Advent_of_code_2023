# This script solves Day 11 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 11.12.2023
import copy
import numpy as np
from itertools import combinations

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()


def cosmic_expansion_tracker(lines):
    """
    Replaces the rows and columns that contain no galaxies with symbols 
    '|' for columns, '-' for rows, and '+' for intersections of rows and columns.
    
    Args:
    lines(list): List of lines in the input file
    
    Returns:
    expanded_universe(list): List of list which has the trackers of where the
                             cosmic expansion occurs.
    """
    universe = [list(line) for line in lines]
    expanded_universe = copy.deepcopy(universe)
    n_columns = len(universe)
    n_rows    = len(universe[0])

    # Expand the columns
    n_added_columns = 0
    for i in range(n_columns):
        column = [a[i:i+1][0] for a in universe] #column
        if set(column) == {'.'}:
            for j in range(n_rows):
               expanded_universe[j][i] = '|'
            print('Column %d needs to expand.' %i)

    # Expand the rows
    n_added_rows = 0
    for i in range(n_rows):
        row = universe[i] #row
        if set(row) == {'.'}:
            for j in range(n_columns):
               identifier = expanded_universe[i][j]
               if identifier == '|':
                  expanded_universe[i][j] = '+'
               else:
                  expanded_universe[i][j] = '-'
            print('Row %d needs to expand.' %i)
    return expanded_universe


def find_galaxies(universe, f_expansion=1):
    """
    Finds the locations of the galaxies after cosmic expansion.

    Args:
    universe: List of list with the trackers of universe expansion
    f_expansion(int): The expansion factor. 
                      e.g. For doubling f_expansion = 2
                           For 10 times expansion f_expansion = 10 etc

    Returns:
    galaxies(dict): The galaxies labeled as numbers and their locations in the universe
                   after cosmic expansion as numpy arrays.
    """
    galaxies   = {}
    f_expansion -= 1
    galaxy_no  = 1
    added_rows = 0
    for y,row in enumerate(universe):
        added_columns = 0
        if row[0] in ['-','+']:
           added_rows += f_expansion
        for x,identifier in enumerate(row):
           if identifier == '#':
              galaxies[galaxy_no] = np.array([y+added_rows,x+added_columns])
              galaxy_no += 1
           elif identifier == '|':
              added_columns += f_expansion
    return galaxies



def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    if part1:
       f_expansion = 2
    else:
       f_expansion = 1000000

    # Add trackers to the rows and columns where there are no galaxies
    universe = cosmic_expansion_tracker(lines)
    if verbose:
        for line in universe:
            print(''.join(line))

    # Get the location of the galaxies
    galaxies = find_galaxies(universe, f_expansion)

    # Get the sum of shortest paths
    shortest_path = 0
    for comb in list(combinations(galaxies,2)):
        a,b = comb[0],comb[1]
        shortest_path += sum(abs(galaxies[a]-galaxies[b]))

    print('The sum of the length of the shortest path between every pair of galaxies is: ', shortest_path)

if __name__ == "__main__":
    main()

