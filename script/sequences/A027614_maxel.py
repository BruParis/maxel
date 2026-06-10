import click
from pathlib import Path
from sympy import symbols, pprint, simplify, factor, together

from maxel.common import A027614_FP
from maxel.sequences import load_and_assign_to
from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType


# This script loads the sequence A027614 and constructs a lower
# triangular matrix with the following formula:
# ...
# Taking the exponential of this matrix yields
# ...
@click.command()
@click.argument("n", type=int)
def cli(n: int):
    # x, _ = symbols("x, y")
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(Path(A027614_FP), list_a)

    # test this is a comment
    def func_expr(i, j):
        sign = (-1) ** (i - j + 1)
        expr_str = f"{sign}*(j+1)*(a{i-j})/factorial(i-j)"
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

    diag_factorial = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    diag_factorial_inv = diag_factorial.inv()
    aux_matrix = diag_factorial * exp_matrix * diag_factorial_inv
    aux_matrix = aux_matrix.applyfunc(factor)
    print(" -> diag_i! * _ * diag_1/i!")
    pprint(aux_matrix)


if __name__ == "__main__":
    cli()  # type: ignore[call-arg]
