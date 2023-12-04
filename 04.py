import numpy as np

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def get_cards(line):
    cards = line.split(':')[1]
    winning_card = cards.split('|')[0].split() 
    your_card = cards.split('|')[1].split() 
    return winning_card, your_card

def find_matches(winning_card, your_card):
    matches =  set(winning_card) & set(your_card)
    return matches

def get_worth(matches):
    if len(matches) == 0:
        worth = 0
    else:
        worth = 1
        for i,match in enumerate(matches):
            if i != 0:
                worth = worth*2
    return worth

def main():

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    answer = 0

    if part1:

        for line in lines:
            winning_card, your_card = get_cards(line)
            matches = find_matches(winning_card, your_card)
            answer += get_worth(matches)
    
        print('The puzzle answer is:', answer)

    else:

        # Numpy array of original set of cards
        n_cards = np.ones(len(lines), dtype = np.int64)

        for i, line in enumerate(lines):
            # How many of the current card do you have?
            n_current_card = n_cards[i]

            winning_card, your_card = get_cards(line)
            matches = find_matches(winning_card, your_card)

            for j,match in enumerate(matches):
               # Each of the current cards win one copy of the next cards
               n_cards[i+j+1] += n_current_card

        answer = int(sum(n_cards))

        print('The total number of scratchcards you end up with is:', answer)

if __name__ == "__main__":
    main()

