# This script solves Day 8 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 08.12.2023
import copy
import math

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def read_nodes(lines):
    connections = {}
    nodes = []
    for line in lines:
        if '=' in line:
            node  = line.split('=')[0].strip()
            nodes.append(node)
            left  = line.split('=')[1].replace('(','').split(',')[0].strip()
            right = line.split('=')[1].replace(')','').split(',')[1].strip()
            connections[node+'L'] = left
            connections[node+'R'] = right
    return nodes, connections

def find_n_steps_part1(node_start, node_end, instructions, connections):
    n_steps = 0
    node = node_start
    while node != node_end:
        for instruction in instructions:
            node = connections[node+instruction]
            n_steps += 1
            if node == node_end:
                break
    return n_steps

def find_n_steps_part2(node_start, instructions, connections):
    n_steps = 0
    node = node_start
    while node[-1] != 'Z':
        for instruction in instructions:
            node = connections[node+instruction]
            n_steps += 1
            if node[-1] == 'Z':
                node_end = node
                break
    return node_end, n_steps



def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    instructions = lines[0]
    nodes, connections = read_nodes(lines)

    if part1:
        n_steps = find_n_steps_part1('AAA','ZZZ',instructions,connections)
        print('The total number of steps required to reach ZZZ is:', n_steps)

    else:
        starting_nodes = []
        for node in nodes:
            if node[-1] == 'A':
                starting_nodes.append(node)

        n_steps_each = []
        for node_start in starting_nodes:
            node_end, n_steps = find_n_steps_part2(node_start,instructions,connections)
            print('From %s to %s it needs %d steps.' %(node_start, node_end, n_steps))
            n_steps_each.append(n_steps)

        print("The total number of steps it takes before you're only on nodes that end with Z is:", math.lcm(*n_steps_each))


if __name__ == "__main__":
    main()

