import click
from pathlib import Path
from sympy import symbols, pprint, simplify, factor, together

from maxel.common import A179320_FP
from maxel.series import load_and_assign_to
from maxel.matrix import matrix_from_func, EMatrixType


# This script loads the sequence A179320 and constructs a lower
# triangular matrix with the following formula:
# (j+1)*a(i-j)/(i-j)!
# Taking the exponential of this matrix yields
# The odd columns of the pascal triangle (column indexed from 0)
# rectified to make a lower triangular matrix
@click.command()
@click.argument("n", type=int)
def main(n: int):
    x, y = symbols("x, y")
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(Path(A179320_FP), list_a)

    # test this is a comment
    def func_expr(i, j):
        expr_str = f"((j+1)*a{i-j})/factorial(i-j)"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)

    print("MATRIX")
    matrix = matrix.applyfunc(factor)
    pprint(matrix)

    print("Evaluate in a")
    matrix = matrix.subs(dict_a)
    matrix = matrix.applyfunc(factor)
    pprint(matrix)

    print("EXP MATRIX")
    exp_matrix = matrix.exp()
    exp_matrix = exp_matrix.applyfunc(factor)
    pprint(exp_matrix)


if __name__ == "__main__":
    main()
