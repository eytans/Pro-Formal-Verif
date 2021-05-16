from z3 import *
import sys


# A variable representing the value of a specific cell
def matrixvar(i, j):
    return Int("x_%s_%s" % (i, j))


# Create a 9x9 matrix of integer variables
def getMatrix():
    return [[matrixvar(i + 1, j + 1) for j in range(9)]
            for i in range(9)]


# Add constraints such that each cell contains a value in {1, ..., 9}
def addCellConstraints(X):
    """
    Commented out the LIA way of solving and instead using inequalities
    :param X: Matrix of z3 variables
    :return: If using LIA a conjunction of LE GE contraints on the variables in the matrix.
             In the case on equality alone a list on inequalities with each number in the range.
             Depending on how int is represented (probably bit set and then no problem)
             I might need a set of equalities to maintain the wanted integers.
             I am adding these just in case.
    """
    # LIA
    # le = [X[i][j] <= 9 for i in range(9) for j in range(9)]
    # ge = [X[i][j] >= 1 for i in range(9) for j in range(9)]
    # return And(*(le + ge))

    # Theory of equality
    eq_constraints = (Or(*(X[i][j] == k for k in range(1, 10))) for i in range(9) for j in range(9))
    return And(*eq_constraints)


# Add constraints such that each row contains a digit at most once
def addRowConstraints(X):
    """
    :param X: Matrix of z3 variables
    :return: :return: And contraint of inequality between all pairs of variables in a row (Good for any theory with equality)
    """
    result = []
    for row in range(9):
        for col1 in range(9):
            for col2 in range(col1 + 1, 9):
                result.append(X[row][col1] != X[row][col2])
    return And(*result)


# Add constraints such that each column contains a digit at most once
def addColumnConstraints(X):
    """
    :param X: Matrix of z3 variables
    :return: And contraint of inequality between all pairs of variables in a column (Good for any theory with equality)
    """
    result = []
    for col in range(9):
        for row1 in range(9):
            for row2 in range(row1 + 1, 9):
                result.append(X[row1][col] != X[row2][col])
    return And(*result)


# Add constraints such that each 3x3 square contains a digit at most once
def addSquareConstraints(X):
    """
    Note: Please use pep8 when using python, pycharm shouts on me.
    I am doing it a little ugly so documenting.
    I am creating an iterator of indices. Then using my helper function I create the constraints and concat.
    :param X: Matrix of z3 variables
    :return: Conjunction of inequalitis between each of the variables in each subgrid.
    """
    import itertools

    def createConstraints(indices):
        return [X[row1][col1] != X[row2][col2]
                for i, (row1, col1) in enumerate(indices) for row2, col2 in indices[i:]
                if row1 != row2 or col1 != col2]

    areas = itertools.product([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    indices = [list(itertools.product(x, y)) for x, y in areas]
    result = And(*itertools.chain(*map(createConstraints, indices)))
    return result


def solveSudoku(instance):
    X = getMatrix()

    # Create the initial constraints of the puzzle
    # based on the input instance. Note that '0' represents 
    # an empty cells
    instance_c = [If(instance[i][j] == 0,
                     True,
                     X[i][j] == instance[i][j])
                  for i in range(9) for j in range(9)]

    # Create the Z3 solver
    s = Solver()

    # Add all needed constraints
    s.add(instance_c)
    s.add(addCellConstraints(X))
    s.add(addRowConstraints(X))
    s.add(addColumnConstraints(X))
    s.add(addSquareConstraints(X))

    # If the problem is satisfiable, a solution exists
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(X[i][j]) for j in range(9)]
             for i in range(9)]
        print_matrix(r)
    else:
        print("failed to solve")
