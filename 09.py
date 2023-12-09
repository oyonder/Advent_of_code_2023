# This script solves Day 9 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 09.12.2023
import copy
import math

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def get_history(line):
    sequence = [int(x) for x in line.split()]
    history = [sequence]
    while set(sequence) != {0}:
        sequence = [(sequence[i+1]-sequence[i]) for i in range(len(sequence) - 1)]
        history.append(sequence)
    return history

def extrapolate_part1(history):
    reverse = copy.deepcopy(history)
    reverse.reverse()
    placeholder = 0
    for sequence in reverse:
        placeholder = placeholder + sequence[-1]
        print('placeholder', placeholder)
    return placeholder


def extrapolate_part2(history):
    reverse = copy.deepcopy(history)
    reverse.reverse()
    placeholder = 0
    for sequence in reverse:
        placeholder = sequence[0] - placeholder
        print('placeholder', placeholder)
    return placeholder


def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    answer = 0
    for line in lines:
        history = get_history(line)
        if part1:
            placeholder = extrapolate_part1(history)
        else:
            placeholder = extrapolate_part2(history)
        answer += placeholder

    print('The sum of the extrapolated values is:', answer)
if __name__ == "__main__":
    main()

