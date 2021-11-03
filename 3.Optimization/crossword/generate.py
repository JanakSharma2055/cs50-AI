import sys
import itertools

from crossword import *
from copy import deepcopy

# TODO two last functions are pending rest is done will implement at the end

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        '''
        domain is a dictonary with form 
        domain={
            Variable:{all the words}
        }
        Variable:properties of particular vertical or horizontal word cells
        (length, direction,starting point)
        '''
        #if any of the words in domain donot match in length with the required 
        #length of variable than it is removed
        for var,values in self.domains.items():
            for value in list(values):
                if len(value) is not var.length:
                    self.domains[var].remove(value)

        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        '''
        let's say two words are hello and mice
        according to this function let's say overlapping_pos_for_x,overlapping_pos_for_y = 2,4
        then all the words in the domain of x are removed which donot
        satisfy this overlapping condition
        '''
        revised = False
        overlapping_pos_for_x, overlapping_pos_for_y = self.crossword.overlaps[x, y]
        for X in set(self.domains[x]):
            # condition that does not cause a conflict
            if any(X[overlapping_pos_for_x] == Y[overlapping_pos_for_y] for Y in self.domains[y]):
                continue
            # removes conflicting values from set of domains of x
            self.domains[x].remove(X)
            revised = True
        return revised
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #pending to see----------
        #using list as queue
        queue = []
        if arcs is None:
            #forming the combination of two items 
            for v1, v2 in itertools.combinations(self.domains, 2):
                if self.crossword.overlaps[v1, v2] is not None:
                    queue.append((v1, v2))
        else:
            queue = arcs

        # Repeat until no more arcs are in the queue
        while queue:

            # Dequeue an arbitrary arc (X, Y) from the queue
            (X, Y) = queue.pop(0)

            # Make X arc-consistent with respect to Y.
            if self.revise(X, Y):

                
                if not self.domains[X]:
                    return False

                # As revise might remove the element which seem to be #inconsistent now but might be needed in later iterations
                #so it needs to be enqueued
                # so enqueue (Z, X) to the queue
                for Z in self.crossword.neighbors(X) - {Y}:
                    queue.append((Z, X))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #the description is a bit misleading
        #the assignment consists of each variable assigned with one single word
        #which needs to be checked if it is consistent 
        #pending to see--------------------
         # checks for constraint that all words must be different
        if len(assignment.values()) != len(set(assignment.values())):
            return False

        # checks for constraint that every word is the correct length
        for variable, word in assignment.items():
            #confused here as the word must be a list and each item should
            #be iterated
            if variable.length != len(word):
                return False

        # checks for constraint that neighbours doesnot conflict the overlap
        for v1, v2 in itertools.combinations(assignment, 2):
            if self.crossword.overlaps[v1, v2] is not None:
                p1, p2 = self.crossword.overlaps[v1, v2]
                if assignment[v1][p1] != assignment[v2][p2]:
                    return False
        
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
         # keeps track of values ruled out among the neighbors of `var`
        counter = {value: 0 for value in self.domains[var]}

        # gets neighboring variables of `var`
        neighbours = self.crossword.neighbors(var)

        for value in self.domains[var]:
            for neighbour in neighbours:

                # ignores neighbour already assigned with a value
                if neighbour in assignment:
                    continue

                # increases counter if value is in domains of neighbour
                if value in self.domains[neighbour]:
                    counter[value] += 1

        # returns list of domains of `var` sorted in ascending order
        #sorting takes place on the basis of value of dict
        return sorted(counter, key=counter.get, reverse=False)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # assignment contains the dictionary for the variables that have 
        #their values assigned
        #this will contain the remaining dict which have values unassigned
        unassigned_variables = self.crossword.variables - set(assignment)
        #print(type(unassigned_variables))

        # tracks number of values in domains of each unassigned variable
        domains = {var: len(self.domains[var]) for var in unassigned_variables}

        # variable(s) with the minimum number of remaining values in its domain
        res = [var for var in domains if domains[var] == min(domains.values())]

        # returns variable with smallest domain
        if len(res) == 1:
            return res[0]

        #in case of tie
        # tracking variable in terms of degree
        degree_of_variables = {var: len(self.crossword.neighbors(var)) for var in res}

        # returns variable with maximum neighbours
        return max(degree_of_variables, key=degree_of_variables.get)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # returns the complete assignment if possible to do so.
        if self.assignment_complete(assignment):
            return assignment

        # unassigned variable based on the MRV and the degree heuristics
        var = self.select_unassigned_variable(assignment)

        # order values based on Least-constraining-value heuristic
        for value in self.order_domain_values(var, assignment):

            # copy self.domains for restoring it, if needed
            domain_copy = deepcopy(self.domains)

            

           

            # check if new assignment is consistent or not
            if self.consistent(assignment):
                # make a new assignment to a variable
                assignment[var] = value

                # if consistent, backtrack for another assignment
                result = self.backtrack(assignment)

                if result is not None:
                    return result

            # if inconsistent, delete assignment and its inferences
            # and also restore self.domains to its previous values
            del assignment[var]
            
            self.domains = domain_copy

        # returns None, if no solution is possible
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
