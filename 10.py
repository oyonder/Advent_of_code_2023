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

def find_next(current, visited, lines):
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

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    start_loc = find_start(lines)
    y0,x0 = start_loc[0], start_loc[1]
    #current = (y0, x0+1) # Right - 
    #end_loc = (y0+1, x0) # Down  | 
    current = (y0-1,x0) # Up    | 
    end_loc = (y0,x0+1) # Right J
    visited = [start_loc, current]

    counter = 2

    while current != end_loc:
        current = find_next(current, visited, lines)
        y,x = current[0],current[1]
        #print('current', current, lines[y][x])
        counter += 1
        visited.append(current)

    print('Total number of steps is', counter)
    print('The farthest point is %d steps away!' %(counter/2))

    answer = count_enclosed_area(lines, visited)
    print(answer)

if __name__ == "__main__":
    main()

