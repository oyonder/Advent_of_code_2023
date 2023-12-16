# This script solves Day 16 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 16.12.2023
import copy
import numpy as np


def read_file(file_name):
    try:
        with open(file_name, "r") as f:

            lines = f.read().strip().split('\n')
            contraption = [list(line) for line in lines]
            return contraption
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def get_start():
    """
    Returns:
    start_locs(list): A list of tuples with the possible location and direction of the entering beam.
    """
    ymax = len(contraption)-1
    xmax = len(contraption[0])-1

    start_locs = []
    
    for y in range(ymax+1):
        start_locs.append((y,0,'R'))    # First column
        start_locs.append((y,xmax,'L')) # Last column

    for x in range(xmax+1):
        start_locs.append((0,x,'D'))    # First row
        start_locs.append((ymax,x,'U')) # Last row

    return start_locs



def get_next(beam):
    """
    Gets the next tile location and its direction.

    Args:
    beam(tuple): (y,x,dir) position and direction of the beam

    Returns:
    next(list): position and direction of next step(s) of the beam
    """
    y0,x0 = beam[0], beam[1]
    d = beam[2]
    tile = contraption[y0][x0]
    next_beams = []
    if tile == '.':
        if   d == 'L':
            next_beams.append((y0,x0-1,d))
        elif d == 'R':
            next_beams.append((y0,x0+1,d))
        elif d == 'U':
            next_beams.append((y0-1,x0,d))
        else:
            next_beams.append((y0+1,x0,d))
    elif tile == '-':
        if   d == 'L':
            next_beams.append((y0,x0-1,d))
        elif d == 'R':
            next_beams.append((y0,x0+1,d))
        else:
            next_beams.append((y0,x0+1,'R'))
            next_beams.append((y0,x0-1,'L'))
    elif tile == '|':
        if   d == 'U':
            next_beams.append((y0-1,x0,d))
        elif d == 'D':
            next_beams.append((y0+1,x0,d))
        else:
            next_beams.append((y0+1,x0,'D'))
            next_beams.append((y0-1,x0,'U')) 
    elif tile == '\\':
        if   d == 'L':
            next_beams.append((y0-1,x0,'U'))
        elif d == 'R':
            next_beams.append((y0+1,x0,'D'))
        elif d == 'U':
            next_beams.append((y0,x0-1,'L'))
        else:
            next_beams.append((y0,x0+1,'R'))
    elif tile == '/':
        if   d == 'L':
            next_beams.append((y0+1,x0,'D'))
        elif d == 'R':
            next_beams.append((y0-1,x0,'U'))
        elif d == 'U':
            next_beams.append((y0,x0+1,'R'))
        else:
            next_beams.append((y0,x0-1,'L'))

    ymax = len(contraption)-1
    xmax = len(contraption[0])-1
    for next_beam in next_beams:
        y,x = next_beam[0],next_beam[1]
        if y < 0 or y > ymax:
            next_beams.remove(next_beam)
        if x < 0 or x > xmax:
            next_beams.remove(next_beam)
    return next_beams 


def bfs(beam0):
    """
    Breadth-First Search algorithm.
    Args:
    beam0(tuple): A tuple, which identifies the location of the beam entering
                  and its traveling direction (y,x,direction) 
  
    Returns:
    visited(list): A list of tuples with the locations of direction of beams traveled. 
    """
    queue = [beam0]
    visited = set([beam0])

    while queue:
        beam = queue.pop(0)

        for next_beam in get_next(beam):
            if next_beam not in visited:
                queue.append(next_beam)
                visited.add(next_beam)
    return visited


def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    global contraption
    contraption = read_file(file_name)

    if part1:
        beam0 = (0,0,'R')
        visited = bfs(beam0)
        visited_coords = {(y,x) for (y,x,d) in visited}
        print('The number of tiles energized is:', len(visited_coords) )

    else:
        beam0s = get_start()
        max_n_tiles = 0
        for beam0 in beam0s:
            visited = bfs(beam0)
            visited_coords = {(y,x) for (y,x,d) in visited}
            n_tiles = len(visited_coords)
            max_n_tiles = max(n_tiles, max_n_tiles)
            print('beam', beam0, 'n_tiles', n_tiles)
        print('The maximum number of tiles energized is:', max_n_tiles )


if __name__ == "__main__":
    main()

