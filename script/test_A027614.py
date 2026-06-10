import click
from sympy import symbols, pprint

from maxel.common import A027614_FP
from maxel.series import load_and_assign_to
from maxel.matrix import matrix_from_func, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n: int):
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(A027614_FP, list_a)
    print(f"dict_a: {dict_a}")

    def func_expr(i, j):
        aux_val = 2 * (j + 1)
        sign = (-1) ** (i - j + 1)
        return f"({aux_val}*{sign}*a{i-j}/factorial(i-j))"

    matrix_log_binomial_2 = matrix_from_func(func_expr, EMatrixType.LOWER, n)

    print("MATRIX")
    pprint(matrix_log_binomial_2)

    print("Evaluate in a")
    matrix_eval = matrix_log_binomial_2.subs(dict_a)
    pprint(matrix_eval)

    print("EXP MATRIX")
    pprint(matrix_eval.exp())


if __name__ == "__main__":
    main()
