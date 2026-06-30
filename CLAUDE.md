# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**maxel** is a mathematical research project exploring OEIS sequences through matrix algebra (specifically matrix logarithms and exponentials of polynomial coefficient matrices — "maxels"). The core idea: represent orthogonal polynomial families (Pascal, Jacobi, Legendre, Hermite, ...) as lower-triangular coefficient matrices, then study their matrix logarithms, which often yield cleaner combinatorial objects.

## Environment

The project uses a local `.venv` at `.venv/`. Always run Python with:

```bash
.venv/bin/python script/path/to/script.py <n>
```

Install the `maxel` package (editable) and dependencies:

```bash
.venv/bin/pip install -e .
```

There is no test suite and no linter configuration.

## Running Scripts

All scripts under `script/` are Click CLI tools that take `n` (matrix size) as a positional argument. Many Jacobi scripts also accept `--mu` and `--nu` options to evaluate at specific parameter values:

```bash
.venv/bin/python script/jacobi/log_jacobi3.py 5
.venv/bin/python script/jacobi/log_jacobi3.py 5 --mu 0 --nu 0
.venv/bin/python script/pascal/log_pascal.py 6
.venv/bin/python script/hermite/log_hermite.py 5
```

Jupyter notebooks live in `notebooks/` and can be launched with:

```bash
.venv/bin/jupyter lab
```

## Code Architecture

### `maxel/` library

- **`matrix.py`** — core matrix construction utilities. Two main entry points:
  - `matrix_from_str(expr_str, matrix_type, n)` — builds an n×n SymPy matrix from a string expression in `i`, `j`
  - `matrix_from_func(func, matrix_type, n)` — builds from a Python callable `func(i, j) -> str` that returns a SymPy-parseable expression string
  - `EMatrixType` enum: `FULL`, `UPPER`, `LOWER`, `DIAGONAL` — controls which entries are zeroed out
- **`sequences.py`** — loads OEIS sequence data from `oeis/*.txt` files and maps them onto SymPy symbol lists
- **`common.py`** — file path constants for the OEIS data files

### Script conventions

Each script follows the same pattern:
1. Define a `func_expr(i, j) -> str` returning a SymPy expression string for the matrix entry
2. Call `matrix_from_func(func_expr, EMatrixType.LOWER, n)` to build the coefficient matrix
3. Apply diagonal similarity transforms (`diag_left * matrix * diag_right.inv()`) to normalize it (e.g. make diagonal all-1s)
4. Call `.log()` on the normalized matrix to get the infinitesimal generator
5. Apply further diagonal transforms to simplify the log matrix
6. `pprint()` intermediate results

### OEIS data (`oeis/`)

Plain text files with space-separated integer sequences. Loaded via `sequences.load_sequences(fp)`. Used in scripts like `jacobi_maxel.py` to substitute EGF coefficients (A027614) into symbolic matrix expressions.

### Key mathematical pattern

For a lower-triangular matrix `M` with nonzero diagonal, the workflow is:
```
M  →  D1 * M * D2.inv()  (normalize to diagonal=I)  →  .log()  →  further diagonal simplification
```

The log of a lower-triangular matrix with all-1 diagonal is computed exactly by SymPy's `.log()`. If the diagonal isn't 1, normalize first with diagonal matrices before taking the log.
