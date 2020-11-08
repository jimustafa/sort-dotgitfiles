from typing import Optional
from typing import Sequence

from sort_git_files import _main
from sort_git_files._utils import _sort_gitattributes


def main(argv: Optional[Sequence[str]] = None) -> int:
    return _main(_sort_gitattributes, argv)


if __name__ == '__main__':
    exit(main())
