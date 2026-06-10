import click
from tqdm import tqdm
import numpy as np
from itertools import combinations
from sympy import Rational, factorial

MAX_N = 15

sequence = [0, 1]


for i in tqdm(range(2, MAX_N)):

    val = 0
    range_idx = list(range(1, i))
    range_val = [sequence[idx] for idx in range_idx]

    for j in range(1, i):

        curr_fact = Rational(1, factorial(j + 1))

        aux = 0
        comb = list(combinations(range_idx, j))

        # comb is lexicographically ordered
        for c in comb:

            comb_idx = [c[0] if k == 0 else c[k] - c[k - 1] for k in range(len(c))]

            comb_val = [sequence[k] for k in comb_idx]

            comb_fact = [(2 * k + 1) for k in c]

            complement_val = sequence[i - sum(comb_idx)]

            aux += complement_val * np.prod(comb_val) * np.prod(comb_fact)

        val += curr_fact * aux

    new_val = 1 - val
    sequence.append(new_val)

print("Sequence:", sequence)

sequence = [factorial(i) * v for i, v in enumerate(sequence)]
print(f"A027614: {sequence}")
