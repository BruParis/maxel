from enum import Enum

from sympy import symbols, Matrix, factor
from sympy.parsing.sympy_parser import parse_expr


class EMatrixType(Enum):
    FULL = "full"
    UPPER = "upper"
    LOWER = "lower"
    DIAGONAL = "diagonal"


def resolve_expr_ij(expr, i, j):
    return expr.subs({"i": i, "j": j})


def eval_func_upper(func):
    def closure(i, j):
        if i > j:
            return 0

        return func(i, j)

    return closure


def eval_func_lower(func):
    def closure(i, j):
        if i < j:
            return 0

        return func(i, j)

    return closure


def eval_func_diagonal(func):
    def closure(i, j):
        if i == j:
            return func(i, j)

        return 0

    return closure


def eval_func_from_matrix_type(func, matrix_type: EMatrixType):
    if matrix_type == EMatrixType.FULL:
        return func
    elif matrix_type == EMatrixType.UPPER:
        return eval_func_upper(func)
    elif matrix_type == EMatrixType.LOWER:
        return eval_func_lower(func)
    elif matrix_type == EMatrixType.DIAGONAL:
        return eval_func_diagonal(func)
    else:
        raise ValueError(f"Matrix type {matrix_type} not supported")


def matrix_from_str(expr, matrix_type, n):
    expr = parse_expr(expr)
    mat = matrix_from_expr(expr, matrix_type, n)
    mat = mat.applyfunc(factor)

    return mat


def matrix_from_expr(expr, matrix_type, n):
    # expr should have i, j as symbols

    def closure(i, j):
        return resolve_expr_ij(expr, i, j)

    eval_func = eval_func_from_matrix_type(closure, matrix_type)

    mat = Matrix(n, n, eval_func)
    mat = mat.applyfunc(factor)

    return mat


def matrix_from_func(func, matrix_type, n):
    # func generates an expression for i, j
    def closure(i, j):
        parsed_expr = parse_expr(func(i, j))
        return resolve_expr_ij(parsed_expr, i, j)

    eval_func = eval_func_from_matrix_type(closure, matrix_type)

    mat = Matrix(n, n, eval_func)
    mat = mat.applyfunc(factor)

    return mat
