import itertools
from typing import List


def _sort(lines: List[str]) -> List[str]:
    key_fnc = lambda s: 0 if s.startswith('#') or len(s) == 0 else 1

    blocks = itertools.groupby(lines, key=key_fnc)

    new_lines = []
    for (key, block) in blocks:
        block = list(block)
        if key == 0:
            new_lines += block
        if key == 1:
            sortable = all(map(lambda line: line[1:].find('*') <= 0, block))

            if sortable:
                new_lines += sorted(block, key=str.lower)
            else:
                new_lines += block

    return new_lines


def _sort_gitattributes(lines: List[str]) -> List[str]:
    return _sort(lines)


def _sort_gitignore(lines: List[str]) -> List[str]:
    return _sort(lines)
