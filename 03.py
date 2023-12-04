import re

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def find_numbers_locations(lines):
    '''
    Returns a dictionary whose elements are list of lists.
    The keys represent indices of rows where there are numbers.
    Each sublist includes the information on
    - the column index of where the number starts
    - the column index of where the number ends
    - the number itself as an integer
    '''
    loc_numbers = {}
    for i, row in enumerate(lines):
        loc_numbers[i] = [
            [tmp.start(0), tmp.end(0), int(tmp.group())] 
            for tmp in re.finditer(r'\d+', row)
        ]
    return loc_numbers

def main():

    part1 = input("Is this the part 1? Y/N ") in ['y', 'Y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)
    loc_numbers = find_numbers_locations(lines)

    answer = 0

    if part1:

        # Find all the numbers around the symbols and store them redundantly in a list called redundant numbers
        redundant_numbers = []
        for i, row in enumerate(lines):
            for j, value in enumerate(row):
                if not (value.isnumeric() or value == '.'):
                    for offset in [-1, 0, 1]:
                        if i + offset in loc_numbers:
                            redundant_numbers.extend(
                                [i, num[0], num[1], num[2]] 
                                for num in loc_numbers[i + offset] 
                                if j - 1 in range(num[0], num[1]) 
                                   or j in range(num[0], num[1]) 
                                   or j + 1 in range(num[0], num[1])
                            )

        # Find unique numbers among these redundant numbers
        tmp = []
        tmp.extend(num for num in redundant_numbers if num not in tmp)
        unique_numbers = tmp

        # Sum them up
        for num in unique_numbers:
            answer += num[3]            
                    
 
    else:

        # Find all the numbers around a gear (*)
        for i, row in enumerate(lines):
            for j, value in enumerate(row):
                if value == '*':
                    numbers = []
                    for offset in [-1, 0, 1]:
                        if i + offset in loc_numbers:
                            numbers.extend(
                                num[2] 
                                for num in loc_numbers[i + offset] 
                                if j - 1 in range(num[0], num[1]) 
                                   or j in range(num[0], num[1]) 
                                   or j + 1 in range(num[0], num[1])
                            )
                    
                    # If around that gear there is exactly two numbers add them to the sum
                    if len(numbers) == 2:
                        gear_ratio = numbers[0] * numbers[1]
                        answer += gear_ratio
    
    print('The puzzle answer is:', answer)

if __name__ == "__main__":

    main()

