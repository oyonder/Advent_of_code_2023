#!/usr/bin/env python3
import regex as re

part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

try:
   f = open("input01.txt", "r")
except:
   f = open(input("Enter the input file name, e.g. input01.txt: "), "r")

"""
A function to find the first numerical value of a string
"""
def get_the_first(text):
    the_first = 0
    found = False
    while not found:
       for char in text.strip():
           try:
               found = True
               the_first = int(char) 
               break
           except:
               continue
    return the_first

answer = 0
numbers = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}

for line in f.read().strip().split('\n'):

    if not part1:
        # Find all the matches which are written as text
        result = re.findall("one|two|three|four|five|six|seven|eight|nine", line, overlapped = True)

        # If there are any, replace them with numbers
        if len(result) == 1:
           line = line.split(result[0])[0] + numbers[result[0]] + line.split(result[0])[-1]
        elif len(result) >= 2:
           line1 = line.split(result[0])[0] + numbers[result[0]] + line.split(result[0])[-1]
           line2 = line.split(result[-1])[0] + numbers[result[-1]] + line.split(result[-1])[-1]
           line = line1 + line2

    # Now find the first and last digit in the modified text line
    first_digit  = get_the_first(line)
    second_digit = get_the_first(line[::-1])

    # Sum them up!
    answer += int(str(first_digit)+str(second_digit))

print("The answer is: ", answer)

