import click
from sympy import pprint

from maxel.matrix import matrix_from_str, EMatrixType


@click.command()
@click.argument("expr", type=str)
@click.argument("n", type=int)
@click.argument(
    "matrix_type",
    type=click.Choice([t.value for t in EMatrixType]),
    default=EMatrixType.FULL.value,
)
def main(expr, n, matrix_type):

    matrix_type = EMatrixType(matrix_type)

    matrix = matrix_from_str(expr, matrix_type, n)
    pprint(matrix)


if __name__ == "__main__":
    main()
