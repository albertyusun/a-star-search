INTRODUCTION
------------

* `Author`: Albert Sun (NetID: as1003)
* `Date`: Sept 21, 2021
* `Course`: CS 570 (Artificial Intelligence) taught at Duke University by Professor Vincent Conitzer in Fall 2021.
* `Assignment`: [HW 1](https://courses.cs.duke.edu/fall21/compsci570/homework1.pdf).

FILES
------------
- `570hw1.py` - the main driver of the code containing functions to run the algorithms for both questions.
- `input_FPK_1.txt` - sample txt file to test code for Question 1.
- `input_FPK_2.txt` - another txt file to test code for Question 1.

COMPILING THE CODE
----------------

Compiling the code requires Python version 3.5+ for the function annotations to work. 


For problem 1, run:

    python 570hw1.py question1_function [filename]

where [file_name] is a placeholder for your input file name (e.g. input_FPK_1.txt). 

For problem 2, run: 
    
    python 570hw1.py question2_function [n]

where [n] is a placeholder for n, the size of the n x n chess board for the super queens problem.

HEURISTICS DISCUSSION
-------------

For `problem 1`, I used the sum of all the tiles' minimum number of knight moves necessary to get from its current 
position to its goal position from this [file](https://courses.cs.duke.edu/fall21/compsci570/fifteens_knight_distance.txt) as my heuristic.
This heuristic creates an optimal solution because it always picks the next step that minimizes the amount
of 'minimal moves' left for each piece on the board, thus minimizing the number of steps required to solve the puzzle.

For `problem 2`, I used the number of pairs of superqueens that attack each other as my heuristic, and I set cost to 0. 
This heuristic creates an optimal solution because it always picks the queen in the next column to minimize the pairs of 
superqueens that attack each other, which is the goal of the problem.
