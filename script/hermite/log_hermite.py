import click
from sympy import pprint, factorial, factor

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):
        # Physicist's Hermite polynomial coefficient (closed form):
        # C[i, j] = (-1)^m * i! / (m! * j!) * 2^j,  m = (i-j)/2
        # Only nonzero when (i-j) is even
        if (i - j) % 2 != 0:
            return "0"
        m = (i - j) // 2
        return f"(-1)**{m} * factorial({i}) / (factorial({m}) * factorial({j})) * 2**{j}"

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    matrix = matrix.applyfunc(factor)
    print("HERMITE maxel")
    pprint(matrix)

    # Diagonal entries are 2^i; normalize by diag(2^j) on the right
    # so that the diagonal becomes all 1s (needed for log)
    def func_expr(i, j):
        return f"2**{j}"

    diag_pow2 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_pow2 = diag_pow2.applyfunc(factor)

    print("*" * 80)
    print("matrix * diag(2^(-j))")
    print("*" * 80)
    aux_matrix = matrix * diag_pow2.inv()
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    print("LOG MATRIX")
    log_matrix = aux_matrix.log()
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)

    print("*" * 80)
    print("DIVIDE factorial(i) ON LEFT")
    print("MULTIPLY factorial(j) ON RIGHT")
    print("*" * 80)
    diag_fact = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    log_matrix = diag_fact.inv() * log_matrix * diag_fact
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)


if __name__ == "__main__":
    main()  # type: ignore[call-arg]
