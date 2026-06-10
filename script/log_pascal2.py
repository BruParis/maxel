import click
from sympy import pprint, simplify, factorial
from itertools import product

from maxel.matrix import matrix_from_func, EMatrixType


# A179320
@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):
        if i == 0 and j == 0:
            return "1"

        num = "factorial(i+j+1)"
        den = "(factorial(2*j+1)*factorial(i-j))"
        expr_str = f"{num}/{den}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    pprint(matrix)

    print("LOG MATRIX")
    log_matrix = matrix.log()
    pprint(log_matrix)

    print("INV MATRIX")
    inv_matrix = matrix.inv()
    pprint(inv_matrix)

    print("LOG INV MATRIX")
    log_inv_matrix = inv_matrix.log()
    pprint(log_inv_matrix)


if __name__ == "__main__":
    main()
