import click
from sympy import pprint, simplify, factorial

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType


# Links to A00245
@click.command()
@click.argument("n", type=int)
def main(n):

    I_m = matrix_from_str("1", EMatrixType.DIAGONAL, n)
    pprint(I_m)

    def func_expr(i, j):

        if i == j:
            return "0"

        num = "factorial(i)"
        den = "(factorial(j)*factorial(i-j))"
        expr_str = f"{num}/{den}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    pprint(matrix)

    I_minus_matrix = I_m - matrix
    I_plus_matrix = I_m + matrix

    cayley_matrix = I_minus_matrix * I_plus_matrix.inv()
    print("CAYLEY MATRIX:")
    pprint(simplify(cayley_matrix))
    exit()

    def func_expr(i, j):

        if (i - j) % 2 == 0:
            return "0"

        i_factor = f"I**({i-j+1})"
        expr_str = f"{i_factor}*(j+1)*(i-j+1)"
        return expr_str

    aux_matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    print("AUX MATRIX:")
    pprint(aux_matrix)


if __name__ == "__main__":
    main()
