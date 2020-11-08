import argparse
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence


def _main(
    _sort_fn: Callable[[List[str]], List[str]],
    argv: Optional[Sequence[str]] = None,
) -> int:
    """"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0

    for filename in args.filenames:
        with open(filename, 'r+') as file_:
            lines = [line.strip() for line in file_.readlines()]
            new_lines = _sort_fn(lines)

            if lines != new_lines:
                print(f'Fixing file `{filename}`')
                file_.seek(0)
                file_.write('\n'.join(new_lines) + '\n')
                file_.truncate()
                retval = 1

    return retval
