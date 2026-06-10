import click
from pathlib import Path
from sympy import symbols, pprint, simplify, factor, together

from maxel.common import A261886_FP
from maxel.sequences import load_and_assign_to
from maxel.matrix import matrix_from_func, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n: int):
    x, y = symbols("x, y")
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(Path(A261886_FP), list_a)

    # test this is a comment
    def func_expr(i, j):
        sign = (-1) ** (i - j + 1)
        if i == j:
            poly = "1"
        else:
            poly = "*".join([f"({3*(j+1)+k}+x)" for k in range(3 * (i - j) - 1)])

        expr_str = f"({sign}*a{i-j}/(factorial(i-j)*{poly}))"
        return expr_str

    log_jacobi = matrix_from_func(func_expr, EMatrixType.LOWER, n)

    print("MATRIX")
    log_jacobi = log_jacobi.applyfunc(factor)
    pprint(log_jacobi)

    print("Evaluate in a")
    log_jacobi = log_jacobi.subs(dict_a)
    log_jacobi = log_jacobi.applyfunc(factor)
    pprint(log_jacobi)

    print("EXP MATRIX")
    matrix_jacobi = log_jacobi.exp()
    matrix_jacobi = matrix_jacobi.applyfunc(factor)
    pprint(matrix_jacobi)


if __name__ == "__main__":
    main()
