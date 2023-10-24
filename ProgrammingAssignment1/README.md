# Programming Assignment 1
Advanced Digital Design (EC 551) @ Boston University
Fall 2023


## Assignment Description
This assignment aimed to create a logic synthesis engine that gets an input boolean function and outputs many things, including the minimized sum of products (SOP), minimized product of sums (POS), the principal implicants, the essential principal implicants, and more.

There are 3 modes of inputting a boolean function with our program:
- Type in the boolean function in SOP format.
- Enter the minterms of the functions.
- Use a [PLA file](fullAdder.pla) that describes the boolean algebra.


## Project Requirements 
The logic synthesis program should be able to return the following:
1. Return the design as a canonical SOP
2. Return the design as a canonical POS
3. Return the design INVERSE as a canonical SOP
4. Return the design INVERSE as a canonical POS
5. Return a minimized number of literals representation in SOP
a. Report on the number of saved literals vs. the canonical version
6. Return a minimized number of literals representation in POS
a. Report on the number of saved literals vs. the canonical version
7. Report the number of Prime Implicants
8. Report the number of Essential Prime Implicants
9. Report the number of ON-Set minterms
10. Report the number of ON-Set maxterm
11. Report all the minterms
12. Report all the maxterms

# Brief Implementation Overview

Given any form of input, the first step was to find all the binary combinations that set the equation to 1. 
Using these combinations, all the implicants and prime implicants were determined. 
To find the Essential Prime Implicants, the Quine McCluskey method was used. 
These were the main steps taken to create the logic synthesizer.

# Demo
