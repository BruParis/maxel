import click
from sympy import symbols, pprint

from maxel.common import A261886_FP
from maxel.series import load_and_assign_to
from maxel.matrix import matrix_from_func, EMatrixType


# This code generate a matrix whose
# log is the A124821 read by rows with alternating signs
# A124821: Number triangle T(n,k)=(-1)^(n-k)*(3k+2)*C(3n+1, n-k)/(2n+k+2).
@click.command()
@click.argument("n", type=int)
def main(n: int):
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(A261886_FP, list_a)

    def func_expr(i, j):
        aux_val = 2 + 3 * (j)
        # aux_val = 2*(j+1)
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
