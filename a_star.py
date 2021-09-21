import copy
import heapq
from typing import Tuple

def find_zero_in_array(array: list) -> Tuple:
    for row_vec in array:
        if 0 in row_vec:
            return (array.index(row_vec), row_vec.index(0))
    raise ValueError("0 is not in list")

def convert_to_array(str_object: str) -> list:
    """Converts strings representing boards into corresponding arrays."""
    return [list(map(int, i.split(','))) for i in str_object.split("\n")]

def convert_to_string(array):
    """Converts boards as arrays into corresponding strings that are easily hashable"""
    return '\n'.join([','.join([str(elem) for elem in i]) for i in array])

def convert_array_to_long_list(array): 
    """
    Takes board in nested list format as input and outputs it as a single un-nested list.
    """
    new_list = []
    for i in array: 
        new_list += i
    return new_list

def h_fifteen(state: str) -> int:
    """
    Return the heuristic value of a specific node. Let i be the position of a value
    before and j be the position of the knight in the right place (desired position). 
    This function will return the sum of the min number of knight moves necessary to 
    get all i values into the right j value in a given board.
    
    For any i<16, j<16, the (16*i+j)th number in the following array is the minimum 
    number of knight moves necessary to get from position i to position j. 
    """
    distances = [0, 3, 2, 5, 3, 4, 1, 2, 2, 1, 4, 3, 5, 2, 3, 2, 3, 0, 3, 2, 2, 3, 2, 1, 1, 2, 1, 4, 2, 3, 2, 3, 2, 3, 0, 3, 1, 2, 3, 2, 4, 1, 2, 1, 3, 2, 3, 2, 5, 2, 3, 0, 2, 1, 4, 3, 3, 4, 1, 2, 2, 3, 2, 5, 3, 2, 1, 2, 0, 3, 2, 3, 3, 2, 1, 2, 2, 1, 4, 3, 4, 3, 2, 1, 3, 0, 3, 2, 2, 3, 2, 1, 1, 2, 1, 4, 1, 2, 3, 4, 2, 3, 0, 3, 1, 2, 3, 2, 4, 1, 2, 1, 2, 1, 2, 3, 3, 2, 3, 0, 2, 1, 2, 3, 3, 4, 1, 2, 2, 1, 4, 3, 3, 2, 1, 2, 0, 3, 2, 3, 3, 2, 1, 2, 1, 2, 1, 4, 2, 3, 2, 1, 3, 0, 3, 2, 4, 3, 2, 1, 4, 1, 2, 1, 1, 2, 3, 2, 2, 3, 0, 3, 1, 2, 3, 4, 3, 4, 1, 2, 2, 1, 2, 3, 3, 2, 3, 0, 2, 1, 2, 3, 5, 2, 3, 2, 2, 1, 4, 3, 3, 4, 1, 2, 0, 3, 2, 5, 2, 3, 2, 3, 1, 2, 1, 4, 2, 3, 2, 1, 3, 0, 3, 2, 3, 2, 3, 2, 4, 1, 2, 1, 1, 2, 3, 2, 2, 3, 0, 3, 2, 3, 2, 5, 3, 4, 1, 2, 2, 1, 4, 3, 5, 2, 3, 0]    
    
    sum_of_distances = 0
    
    current_state_list = convert_array_to_long_list(convert_to_array(state))
    
    # i is the current position, j is the value of the number at that given tile currently
    for index, value in enumerate(current_state_list, start=1): 
        desired_spot = value
        min_distance = distances[16 * (index-1) + (desired_spot-1)]
        if value == 0: # you don't try to move "0", because 0 is a blank spot, so no min_distance should be calculated
            min_distance = 0 
        sum_of_distances += min_distance
    return sum_of_distances

def get_possible_states(current_state_str: str) -> list:
    """
    Inputs a nested list representing the current state. Returns list of str 
    representing all possible states from a given state after possible
    knight moves.
    """
    current_state = convert_to_array(current_state_str)
    
    zero_position = find_zero_in_array(current_state)
    knight_moves = [(2, 1), (2, -1), 
                    (-2, 1), (-2, -1), 
                    (1, 2), (1, -2), 
                    (-1, 2), (-1, -2)]

    possible_moves = []

    for knight_move in knight_moves: 
        placement = tuple(item1 + item2 for item1, item2 in zip(knight_move, zero_position))
        in_bounds = (placement[0] >= 0 and placement[0] < 4) and (placement[1] >= 0 and placement[1] < 4)
        if in_bounds: 
            possible_moves.append(placement)

    possible_states = []
    for possible_move in possible_moves:
        i, j = possible_move

        old_value = current_state[i][j]
        new_state = copy.deepcopy(current_state)

        # swap number with the empty spot (0) 

        new_state[i][j] = 0
        new_state[zero_position[0]][zero_position[1]] = old_value

        possible_states.append(convert_to_string(new_state))
  
    return possible_states


def get_prev_moves(current_state: str, prev_state: dict) -> list:
    """
    Given the current state and dictionary of previous moves, return all an ordered list of all
    moves it took to get to that point.
    """
    sequence_list_backwards = []
    sequence_list_backwards.append(current_state)
    while current_state in prev_state:
        current_state = prev_state[current_state]
        sequence_list_backwards.append(current_state)
    sequence_list = sequence_list_backwards[::-1]

    return sequence_list

def a_star_fifteens(initial_state: str) -> list:
    """
    Takes string representing array of fifteens knight problem and returns a list of 
    string turns that solves the problem.

    Example of input: "10,11,3,13\n5,4,1,2\n9,8,6,12\n0,14,15,7"
    """
    g = {} #k: state, v: num moves it took to get there
    prev_state = {} #k: current state, v: prev state
    final_state = '1,2,3,4\n5,6,7,8\n9,10,11,12\n13,14,15,0'
    g[initial_state] = 0
    frontier = [] # priority queue, first thing in the tuple is the f value, second thing in the tuple is the string itself
    heapq.heappush(frontier, (h_fifteen(initial_state), initial_state))

    while frontier: # while heap is not empty (if empty, you've gone through all the possible states)
        current_state = heapq.heappop(frontier)[1]
        if current_state == final_state:
            return get_prev_moves(current_state, prev_state)
        possible_states = get_possible_states(current_state)

        for possible_state in possible_states:
            if possible_state not in g:
                
                prev_state[possible_state] = current_state
                
                g[possible_state] = g[current_state] + 1
                
                f = h_fifteen(possible_state) + g[possible_state] + 1
                heapq.heappush(frontier, (f, possible_state))

sequence_list = a_star_fifteens("10,11,3,13\n5,4,1,2\n9,8,6,12\n0,14,15,7")

for sequence in sequence_list:
    print(f'---------')
    print(sequence)