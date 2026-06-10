import click
from sympy import pprint

from maxel.matrix import matrix_from_str, EMatrixType

matrix_type_str = click.Choice([t.value for t in EMatrixType])


@click.command()
@click.argument("expr", type=str)
@click.argument("n", type=int)
@click.argument("matrix_type", type=matrix_from_str, default=EMatrixType.FULL.value)
def main(expr, n, matrix_type):

    matrix_type = EMatrixType(matrix_type)

    matrix = matrix_from_str(expr, matrix_type, n)
    pprint(matrix)

    print("EXP MATRIX")
    pprint(matrix.exp())


if __name__ == "__main__":
    main()
