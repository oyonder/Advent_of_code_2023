# This script solves Day 6 of Advend of Code 2023
# Author: Özlem Yönder
# Date: 06.12.2023

import numpy as np

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def get_times_and_distances(lines):
    for line in lines: 
        if 'Time:' in line:
            times = [int(x) for x in line.split(':')[1].split()]
        if 'Distance' in line:
            distances = [int(x) for x in line.split(':')[1].split()]
    return times, distances

def count_positive_elements(arr):
    positive_elements = list(filter(lambda x: x > 0, arr))
    return len(positive_elements)

def get_n_winning_ways(t_race, d_record):
    n_config = len(range(t_race))
    t_hold = np.arange(0,t_race,1)
    t_left = np.ones(n_config)*t_race - t_hold
    v = t_hold
    d_test = v*t_left
    difference = d_test - np.ones(n_config)*d_record
    n_winning_ways = count_positive_elements(difference)
    return n_winning_ways

def main():

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    answer = 1

    times, distances = get_times_and_distances(lines)

    if part1:
   
        for t_race,d_record in zip(times, distances):
            n_winning_ways = get_n_winning_ways(t_race, d_record)
            if n_winning_ways != 0:
                answer *= n_winning_ways  

        print('The multiplication of number of ways you can win each game is:', answer)

    else:
        
        t_race = int(''.join([str(x) for x in times]))
        d_record = int(''.join([str(x) for x in distances]))
        print(t_race, d_record)
        n_winning_ways = get_n_winning_ways(t_race, d_record)
        print('The number of winning ways is:', n_winning_ways)


if __name__ == "__main__":
    main()

