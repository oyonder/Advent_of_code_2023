# This script solves Day 15 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 15.12.2023
import copy
import numpy as np


def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split(',')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def HASH_algorithm(word):
    current_value = 0
    for character in word:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lenses = read_file(file_name)

    if part1:
        answer = 0
        for lens in lenses:
            answer += HASH_algorithm(lens)
        print('The sum of the results is: ', answer)

    else:
        boxes_dict = {k: [] for k in range(256)}
        for current_lens in lenses:
            if '=' in current_lens:
                label = current_lens.split('=')[0]
                box_no = HASH_algorithm(label)
                replaced = False
                for i,lens in enumerate(boxes_dict[box_no]):
                    if label in lens:
                        boxes_dict[box_no].remove(lens)
                        boxes_dict[box_no].insert(i,current_lens)
                        replaced = True
                if not replaced: boxes_dict[box_no].append(current_lens)
            else:
                label = current_lens.split('-')[0]
                box_no = HASH_algorithm(label)
                for lens in boxes_dict[box_no]:
                    if label in lens:
                        boxes_dict[box_no].remove(lens)

        answer = 0
        for box in boxes_dict:
            for i,lens in enumerate(boxes_dict[box]):
                power = (box + 1)*(i + 1)*int(lens.split('=')[1])
                answer += power
                print(lens,power)

        print('Focusing power is ', answer)
if __name__ == "__main__":
    main()

