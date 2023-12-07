# This script solves Day 7 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 07.12.2023

import copy

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()


def main():

    verbose = False

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)

    card_types = {'2':0,'3':1,'4':2,'5':3,'6':4,'7':5,'8':6,'9':7,'T':8,'J':9,'Q':10,'K':11,'A':12}
    if not part1:
        card_types['J'] = -1

    hand_types = {(1,1,1,1,1):0,(1,1,1,2):1,(1,2,2):2,(1,1,3):3,(2,3):4,(1,4):5,(5,):6}

    # Read the data such that each card is a tuple of its values and store the corresponding bid
    bids  = {}
    hands_dict = {}
    for line in lines:
        # Read the hand as a list with numbers representation
        hand_tmp = line.split()[0]
        hand_list = []
        for card in hand_tmp:
            hand_list.append(card_types[card])

        # Now determine the hand type and insert its value to the beginning of the hand list
        card_labels = set(hand_list)
        hand_type = []
        if part1:
            for label in card_labels:
                count = hand_list.count(label)
                hand_type.append(count)
            hand_type.sort()
            hand_type = tuple(hand_type)
        else:
            # First count all the cards which are not J
            for label in card_labels:
                if label != -1:
                    count = hand_list.count(label)
                    hand_type.append(count)
            hand_type.sort()
            # Then modify the hand type for the optimal configuration
            J_count = hand_list.count(-1)
            if hand_type != []:
                hand_type[-1] += J_count
            else:
                hand_type.append(J_count)
            hand_type = tuple(hand_type)

        hand_list.insert(0,hand_types[hand_type])

        # Add the representation of hand to the bids dictionary
        hand = tuple(hand_list)
        bid  = int(line.split()[1])
        bids[hand] = bid
        hands_dict[hand] = hand_tmp

    # Now sort all the hands
    n_cards = len(lines[0].split()[0])
    sorted_hands = copy.deepcopy(bids)
    for i in range(n_cards+1):
        if verbose: print('Sorting according to the %dth digit.' %i)
        sorted_hands = sorted(sorted_hands, key=lambda card: card[n_cards-i])

    # Calculate the total winnings
    total_winnings = 0
    for i,hand in enumerate(sorted_hands):
        rank = i+1
        total_winnings += rank * bids[hand]
        if verbose: print('Rank:', rank, 'Bid:', bids[hand], 'Hand:', hands_dict[hand])

    print('The total winnings are: ', total_winnings) 

if __name__ == "__main__":
    main()

