import math
from functools import lru_cache
from sympy import binomial, factorial

MAX_N = 20


@lru_cache(maxsize=None)
def T(n, k):  # T = A123521
    if k == 0:
        return 1
    elif k == 1:
        return 2 * (n - 1)
    else:
        return T(n - 2, k - 2) + binomial(2 * n - k - 1, 2 * n - 2 * k - 1)


@lru_cache(maxsize=None)
def b(n):
    if n == 1:
        return 1

    total = 0
    list_range = list(range(2, 2 * (n // 2) + 1))
    for j in list_range:
        total += T(n, j) * b(n - j + 1)

    return (-1 / (2 * (n - 1))) * total


def A027614(n):
    sign = (-1) ** (n + 1)
    return sign * factorial(n) * b(n)


sequence = [A027614(i) for i in range(1, MAX_N)]
print("A027614:", sequence)
