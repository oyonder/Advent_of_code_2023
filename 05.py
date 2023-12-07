# This script solves Day 5 of Advent of Code 2023
# Author: Özlem Yönder
# Date: 05.12.2023

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip().split('\n')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()

def get_y(x, identifier, lines):
    """
    Extracts the corresponding numbers based on mapping information provided in the file.
    Args:
    - x : source number
    - identifier (str): The identifier to search for.
    - lines (list): List of lines from the file.

    Returns:
    - y : corresponding destination number
    """

    in_mapping_section = False
    y = x
    for i, line in enumerate(lines):

        if identifier+' map:' in line:
            in_mapping_section = True

        if in_mapping_section:
            try:
                if lines[i+1] == '':
                    break

                destination_start,source_start,range_length = map(int, lines[i+1].split())
                if x in range(source_start,source_start+range_length):
                    dx = x - source_start
                    y = destination_start + dx

            except IndexError:
                # End of file
                pass
    return y


def read_mapping(identifier, lines):

    in_mapping_section = False
    x_y_ranges  = []

    for i, line in enumerate(lines):

        if identifier+' map:' in line:
            in_mapping_section = True

        if in_mapping_section:
            try:
                if lines[i+1] == '':
                    break

                destination_start,source_start,range_length = map(int, lines[i+1].split())

                x_y_ranges.append((destination_start,source_start,range_length))

            except IndexError:
                # End of file
                pass

    return x_y_ranges


def find_intersection(tuple1, tuple2):
    """
    Finds intersection of two tuples.
    Args:
    - tuple1: (start1, end1)
    - tuple2: (start2, end2)

    Returns:
    - (intersection_start, intersection_end) or None
    """
    start1, end1 = tuple1
    start2, end2 = tuple2

    # Find the maximum of the two start values and the minimum of the two end values
    intersection_start = max(start1, start2)
    intersection_end = min(end1, end2)

    # Check if there is a valid intersection
    if intersection_start <= intersection_end:
        return (intersection_start, intersection_end)
    else:
        return None


def merge_tuples(tuple_list):
    # Sort the list of tuples based on the start value of each tuple
    sorted_tuples = sorted(tuple_list, key=lambda x: x[0])
    
    merged_list = []
    current_tuple = sorted_tuples[0]

    for start, end in sorted_tuples[1:]:
        if start <= current_tuple[1]:  # Check for overlap
            current_tuple = (current_tuple[0], max(current_tuple[1], end))
        else:
            merged_list.append(current_tuple)
            current_tuple = (start, end)

    merged_list.append(current_tuple)

    return merged_list


def find_difference(ranges1, ranges2, verbose=False):
    """
    Finds the intersections and difference between ranges1 and ranges2.
    Args:
    - ranges1 (list): A list of tuples with the ranges of the category which will be mapped onto
    - ranges2 (list): A list of tuples with the ranges of mapping information

    Returns:
    - differences   (list): The intervals as a list of tuples in which ranges1 does not intersect with ranges2.
    - intersections (list): The intervals as a list of tuples in which ranges1 intersects with ranges2.
    """
    intersections = []
    differences   = []
    ranges1.sort()
    ranges2.sort()

    # Find the intersections of ranges1 with ranges2
    for range1 in ranges1:

        for range2 in ranges2:
            intersection = find_intersection(range1, range2)

            if intersection is not None:
                intersections.append(intersection)

    # Find the gaps of ranges2 from -inf to inf
    anti_ranges2 = []
    start = -float('inf')
    for i,range2 in enumerate(ranges2):
        end   = range2[0]
        if end-start > 1:
            anti_ranges2.append((start,end))
        start = range2[1]
    anti_ranges2.append((start,float('inf')))

    # Find the differences by taking the intersections of ranges1 with anti_ranges2
    for range1 in ranges1:

        for anti_range2 in anti_ranges2:
            difference = find_intersection(range1, anti_range2)

            if difference is not None:
                differences.append(difference)

    return differences, intersections


def get_locations_range(seed_ranges, lines, verbose=False):
    """
    Returns the ranges of locations corresponding to the given seed ranges.
    Args:
    - seed_ranges (list): Range of seeds as a list of tuples[(start, range_length), ...]
    - lines       (list): Lines of the input file
    - x_ranges    (list): A list of tuples of the form [(x_min,x_max), ...]
    - y_ranges    (list): A list of tuples of the form [(y_min,y_max), ...]

    Returns:
    - locations (list): A list of tuples with the location ranges where the seeds provided by seed_ranges will be seeded.
    """
    categories = ['seed','soil','fertilizer','water','light','temperature','humidity','location']
    xy = [(categories[i], categories[i + 1]) for i in range(len(categories) - 1)]

    # Get the ranges for the categories seed in the form [(start,end),...]
    x_ranges = []
    for [start_seed, range_length] in seed_ranges:
        x_ranges = merge_tuples(x_ranges + [(start_seed, start_seed + range_length - 1)])

    # Loop over categories and find the corresponding y_ranges based on the mapping information and x_ranges
    for [x,y] in xy:

        y_ranges = []

        identifier = x+'-to-'+y
        print('---------------------')
        print('Mapping based on', identifier)
 
        # Get the ranges for mapping [(start,end),...]
        x_mapping_ranges = []
        for (y_mapping_start, x_mapping_start, range_mapping) in read_mapping(identifier, lines):
            x_mapping_range = (x_mapping_start, x_mapping_start + range_mapping - 1)
            x_mapping_ranges.append(x_mapping_range)
 
        # Differences will be mapped as is and the intersections will be shifted according to the mapping information
        differences, intersections = find_difference(x_ranges, x_mapping_ranges)

        if verbose:
            print('x_ranges', x_ranges)
            print('x_mapping_ranges', x_mapping_ranges)
            print('differences', differences)
            print('intersections', intersections)

        # Find the corresponding y_ranges
        for x_range in differences+intersections:
            y_start = get_y(x_range[0], identifier, lines)
            y_range = (y_start, y_start + x_range[1] - x_range[0])
            y_ranges = merge_tuples(y_ranges+[y_range])

        if verbose: print('The ranges of corresponding %s are' %y, y_ranges)

        # Update x_ranges for the next iteration of categories
        x_ranges = y_ranges 

        # Here is the locations!!!
        if y == 'location':
            locations = y_ranges
        
    return locations


def main():

    part1 = input("Is this for part 1? Y/N: ") in ['Y','y']

    file_name = input("Enter the input file name, e.g. input.txt: ")
    lines = read_file(file_name)
#    lines.remove('')

    verbose = False

    # Get the seeds
    seeds = [int(seed) for seed in lines[0].split(':')[1].split()]

    if part1:
        locations = []
        # Simply looping over seeds work for this part
        for seed in seeds:
            soil        = get_y(seed,        'seed-to-soil'           , lines ) 
            fertilizer  = get_y(soil,        'soil-to-fertilizer'     , lines )
            water       = get_y(fertilizer,  'fertilizer-to-water'    , lines )
            light       = get_y(water,       'water-to-light'         , lines )
            temperature = get_y(light,       'light-to-temperature'   , lines )
            humidity    = get_y(temperature, 'temperature-to-humidity', lines )
            location    = get_y(humidity,    'humidity-to-location'   , lines )
            locations.append(location)
            if verbose: print('Seed %d, soil %d, fertilizer %d, water %d, light %d, temperature %d, humidity %d, location %d.' %(seed,soil,fertilizer,water,light,temperature,humidity,location)) 
        print('=====================')
        print('The lowest location number that corresponds to any of the initial seed numbers is: ', min(locations))
        print('=====================')


    else:

        # Work with ranges instead of looping over each seed
        seed_ranges = [(seeds[i], seeds[i+1]) for i in range(0,len(seeds),2)]

        # Get the corresponding ranges of locations
        locations = get_locations_range(seed_ranges, lines)

        # Find the minimum location
        min_location = float('inf')
        for location in locations:
            min_location = min(min_location, location[0])
        print('=====================')
        print('The lowest location number that corresponds to any of the initial seed numbers is: ', min_location)
        print('=====================')


if __name__ == "__main__":
    main()

