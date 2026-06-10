import click
from sympy import pprint, simplify, factorial, factor, pretty, RisingFactorial
from sympy import symbols as sym
from itertools import product

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType, symbols


@click.command()
@click.argument("n", type=int)
@click.option("--mu", type=int, default=None)
@click.option("--nu", type=int, default=None)
def main(n, mu, nu):

    def func_expr(i, j):
        poly_mu = f"RisingFactorial(mu+{j+1},{i-j})/factorial(i-j)"
        poly_mu_nu = f"RisingFactorial(mu+nu+{i+1},{j})/factorial(j)"

        expr_str = f"{poly_mu}*{poly_mu_nu}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    matrix = matrix.applyfunc(factor)
    print("JACOBI maxel")
    pprint(matrix)

    def func_expr(i, j):
        poly_str = f"factorial({j})"
        return poly_str

    diag_1 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_1 = diag_1.applyfunc(factor)
    pprint(diag_1)

    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+{i+1},{j})"
        return poly_str

    diag_2 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_2 = diag_2.applyfunc(factor)
    pprint(diag_2)

    print("*" * 80)
    print("diag_1 * matrix * diag_2.inv()")
    print("*" * 80)
    aux_matrix = diag_1 * matrix * diag_2.inv()
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    if mu is not None or nu is not None:
        mu_sym, nu_sym = sym("mu nu")
        subs = {}
        if mu is not None:
            subs[mu_sym] = mu
        if nu is not None:
            subs[nu_sym] = nu
        aux_matrix = aux_matrix.subs(subs)
        aux_matrix = aux_matrix.applyfunc(factor)
        print(f"EVALUATED ({', '.join(f'{k}={v}' for k, v in subs.items())})")
        pprint(aux_matrix)
        # Evaluating with mu=0, nu=0 returns the even columns
        # (starting at 0) of the Harriot-Pascal matrix !
        exit()

    print("LOG MATRIX")
    log_matrix = aux_matrix.log()
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)

    def func_expr(i, j):
        poly = f"RisingFactorial(mu+nu+1,{2*j+1})"

        poly_aux = f"({2*i+1}+mu+nu)"
        expr_str = f"({poly})/({poly_aux})"
        return expr_str

    diag_mu_nu_0 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)

    def func_expr(i, j):
        poly = f"RisingFactorial(mu+nu+1,{2*j})"

        poly_aux = f"({2*j+1}+mu+nu)"
        expr_str = f"({poly}*{poly_aux})"
        return expr_str

    diag_mu_nu_1 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    log_matrix = diag_mu_nu_0 * log_matrix * diag_mu_nu_1.inv()
    log_matrix = log_matrix.applyfunc(factor)
    print("SIMPLIFIED LOG MATRIX")
    pprint(log_matrix)

    print("*" * 80)
    print("DIVIDE 1/factorial(j) ON RIGHT")
    print("DIVIDE factorial(i) ON LEFT")
    print("*" * 80)
    diag_fact = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    log_matrix = diag_fact.inv() * log_matrix * diag_fact
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)


if __name__ == "__main__":
    main()  # type: ignore[call-arg]
