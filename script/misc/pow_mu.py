import click
from sympy import symbols, pprint, factor

from maxel.common import A027614_FP
from maxel.sequences import load_and_assign_to
from maxel.matrix import matrix_from_func, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n):
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(A027614_FP, list_a)

    def func_expr(i, j):
        if i == j:
            return "0"

        sign = (-1) ** (i - j + 1)
        return f"({sign}*a{i-j})"

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    matrix = matrix.applyfunc(factor)
    print("ORIGINAL MATRIX")
    pprint(matrix)

    aux_matrix = matrix.copy()
    for k in range(n - 1):
        aux_matrix = aux_matrix * matrix
        aux_matrix = aux_matrix.applyfunc(factor)

        print(f"MATRIX^{k+2}")
        pprint(aux_matrix)


if __name__ == "__main__":
    main()
