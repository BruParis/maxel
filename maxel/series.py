from pathlib import Path
from typing import Union, List, Dict
from sympy import symbols


def load_series(series_fp: Union[Path, str]) -> List[int]:

    with open(series_fp, "r") as f:
        series = f.read()
        list_numbers_str = series.split()
        list_numbers = [int(x) for x in list_numbers_str]

    return list_numbers


def load_and_assign_to(
    serie_fp: Union[Path, str], list_symbols: List[symbols]
) -> Dict[symbols, int]:
    list_numbers = load_series(serie_fp)
    # restrict the list of symbols to the length of the series
    if len(list_symbols) > len(list_numbers):
        list_symbols = list_symbols[: len(list_numbers)]

    if len(list_symbols) < len(list_numbers):
        list_numbers = list_numbers[: len(list_symbols)]

    return dict(zip(list_symbols, list_numbers))
