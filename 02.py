#!/usr/bin/env python3

part1 = input("Is this for part 1? Y/N: ") in ['Y','y']
part2 = not part1

try:
    f = open("input02.txt", "r")
except:
    f = open(input("Enter the input file name, e.g. input02.txt: "), "r")


verbose = False

max_n_red   = 12
max_n_green = 13
max_n_blue  = 14

impossible_games_list = []
total = 0


# Loop over games
for game in f.read().strip().split('\n'):

    game_no = int(game.split(':')[0].split('Game')[1])

    # For part 1, the variable 'total' is the sum of game numbers
    # For part 2, the variable 'total' total is the sum of power of the sets
    if part1: total += game_no

    # The list of sets in a game
    sets = game.split(':')[1].split(';')

    # For part 2, initiate the maximum number of cubes encountered in the game
    n_red_max, n_blue_max, n_green_max = 0, 0, 0

    # Loop over set of cubes for each set in the game
    for set_of_cubes in sets:

        if verbose: print('Set of cubes:', set_of_cubes)

        # For part 2, initiate the number of cubes encountered in the set
        n_red, n_blue, n_green = 0, 0, 0

        for cubes in set_of_cubes.split(','):

            n_cubes = int(cubes.split()[0])

            # For part 1, find out if the game is impossible and if so add it to a list
            if part1:
                 if 'red' in cubes and n_cubes > max_n_red:
                     impossible_games_list.append(game_no)
                 elif 'blue' in cubes and n_cubes > max_n_blue:
                     impossible_games_list.append(game_no)
                 elif 'green' in cubes and n_cubes > max_n_green:
                     impossible_games_list.append(game_no)

            # For part 2, get the number of cubes in that set
            else:
                if 'red' in cubes:
                    n_red = n_cubes
                elif 'blue' in cubes:
                    n_blue = n_cubes
                elif 'green' in cubes:
                    n_green = n_cubes

        # For part 2, keep the maximum number of cubes encountered until now in this game
        n_red_max, n_blue_max, n_green_max = max(n_red_max, n_red), max(n_blue_max, n_blue), max(n_green_max, n_green)

    if verbose: print('The game %d could have been played with a minimum of %d red, %d blue, %d green cubes.' %(game_no, n_red_max, n_blue_max, n_green_max))
    
    if part2: 
         power_of_the_set = n_red_max*n_blue_max*n_green_max
         total += power_of_the_set

if part1:
    impossible_games = set(impossible_games_list)
    
    answer = total - sum(impossible_games)
    
    print('The sum of IDs of possible games: ', answer)

else:
    print('The sum of the power of these sets: ', total)
