# This script solves Day 10 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 10.12.2023

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def find_start(lines):
    for y,line in enumerate(lines):
        for x,pipe in enumerate(line):
            if pipe == 'S':
                 return (y,x)
    return None


def find_two_possibilities(start_loc, lines):
    """
    Finds the two possibilites near the starting location.
    One will be the starting point, the other one will be the end point.

    Args:
    start_loc(tuple): starting location (where 'S' is)
    lines(list): the lines in the files

    Returns:
    two_possibilities: returns tuples with the two possible 
                       directions to go from the starting locaion. 
    """
    y0,x0 = start_loc[0], start_loc[1]
    two_possibilities = []
    # Up
    if lines[y0-1][x0] in ['F','|','7']:
        two_possibilities.append((y0-1,x0))
    # Down
    if lines[y0+1][x0] in ['L','|','J']:
        two_possibilities.append((y0+1,x0))
    # Left
    if lines[y0][x0-1] in ['-','F','L']:
        two_possibilities.append((y0,x0-1))
    # Right
    if lines[y0][x0+1] in ['L','-','J']:
        two_possibilities.append((y0,x0+1))
    return two_possibilities[0], two_possibilities[1]


def find_next(current, visited, lines):
    """
    Finds the next element given the current location.
    
    Args:
    current(tuple): Location of the current pipe
    visited(list): List of tuples with the location of the visited pipes which make up the loop
    lines(list): The lines of the input file

    Returns:
    (y,x): The location of the next pipe as a tuple
    """
    y,x = current[0], current[1]
    current_pipe = lines[y][x]

    # Vertical pipe
    if current_pipe == '|':
        # Up   7, F, | or Down L, J, |
        if (y-1,x) not in visited:
            return (y-1,x)
        else:
            return (y+1,x)

    # Horizontal pipe
    elif current_pipe == '-':
        # Right 7, J, - or Left F, L, -
        if (y,x+1) not in visited:
            return (y,x+1)
        else:
            return (y,x-1)

    # North East, 90-degree bend
    elif current_pipe == 'L':
        # Up or Right
        if (y-1,x) not in visited:
            return (y-1,x)
        else:
            return (y,x+1)

    # North West, 90-degree bend
    elif current_pipe == 'J':
        # Up or Left
        if (y-1,x) not in visited:
            return (y-1,x)
        else:
            return (y,x-1)

    # South West, 90-degree bend
    elif current_pipe == '7':
        # Down or Left
        if (y+1,x) not in visited:
            return (y+1,x)
        else:
            return (y,x-1)

    # South East, 90-degree bend
    elif current_pipe == 'F':
        # Right -, J or Down |
        if (y,x+1) not in visited:
            return (y,x+1)
        else:
            return (y+1,x)

def count_enclosed_area(lines,visited):
    """
    Finds whether a point is inside or outside of the area enclosed using
    ray casting algorithm (also known as crossing number algorithm or even-odd rule algorithm).
    Then, counts the number of points inside the enclosed area.

    Args:
    lines(list): The lines in the input file
    visited(list): A list of tuples, which are the locations of the points which make up the loop

    Returns:
    counter(int): The total number of points inside the enclosed area
    """
    counter = 0
    last_pipe = '|'
    for y,line in enumerate(lines):
        n_crossings = 0
        for x,pipe in enumerate(line):
            if (y,x) in visited:
                if pipe == '|':
                    n_crossings += 1
                elif pipe == 'J':
                    if last_pipe == 'F':
                        n_crossings += 1
                elif pipe == '7':
                    if last_pipe == 'L':
                        n_crossings += 1
                if pipe in ['J','F','L','7']:
                    last_pipe = pipe
            else:
                if n_crossings % 2 != 0:
                     counter += 1
    return counter

 

def main():

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    # Find the location of the starting pipe 
    start_loc = find_start(lines)
    # Find the two possiblities of movement from the start
    current, end_loc = find_two_possibilities(start_loc, lines)

    # Make a list of visited locations which make up the loop and count the number of steps
    visited = [start_loc, current]
    counter = 2
    while current != end_loc:
        current = find_next(current, visited, lines)
        y,x = current[0],current[1]
        counter += 1
        visited.append(current)

    # Part 1
    print('Total number of steps is', counter)
    print('The farthest point is %d steps away!' %(counter/2))

    # Part 2
    print('The number of tiles enclosed by the loop is', count_enclosed_area(lines, visited))

if __name__ == "__main__":
    main()

