import click
from sympy import pprint, simplify, factorial, factor, pretty, RisingFactorial
from itertools import product

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType, symbols


# A027614 can be recovered in the log of legendre coeff. matrix
@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):

        if (i - j) % 2 != 0:
            return "0"

        k_str = f"({(i - j)//2})"
        sign = f"(-1)**({k_str})"
        num = "factorial(i+j)"
        den = f"(2**i)*factorial(i - {k_str})*factorial(j)*factorial({k_str})"
        expr_str = f"{sign}*{num}/({den})"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    matrix = matrix.applyfunc(factor)
    pprint(matrix)

    def func_expr(i, j):
        num = "factorial(2*i)"
        den = "(2**i)*factorial(i)*factorial(i)"
        expr_str = f"{num}/({den})"
        return expr_str

    diag = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag = diag.applyfunc(factor)
    pprint(diag)

    print("*" * 80)
    print("DIVIDE DIAGONAL 2i!/(2^i.i!i!) ON RIGHT")
    print("*" * 80)
    aux_matrix = matrix * diag.inv()
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    print("*" * 80)
    print("LOG MATRIX")
    print("*" * 80)
    log_matrix = aux_matrix.log()
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)

    def func_expr(i, j):

        if i != j:
            return "0"

        expr_str = "factorial(i//2)"
        return expr_str

    diag = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag = diag.applyfunc(factor)
    pprint(diag)

    print("*" * 80)
    print("MULT DIAGONAL (i/2)! ON LEFT")
    print("*" * 80)
    aux_matrix = diag * log_matrix
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    def func_expr(i, j):

        num = "2*((i+2)//2)"
        den = "((i+2)//2)*(2*i+1)*factorial((i+2)//2)"
        expr_str = f"{num}/({den})"
        return expr_str

    diag = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag = diag.applyfunc(factor)
    pprint(diag)

    print("*" * 80)
    print("MULT DIAGONAL ((i+2)/2) ON RIGHT")
    print("*" * 80)
    aux_matrix = aux_matrix * diag
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)


if __name__ == "__main__":
    main()
