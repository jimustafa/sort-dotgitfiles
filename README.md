sort-gitfile
============

A `pre-commit` hook for sorting `.gitignore` and `.gitattributes` files.
This can be useful way to keep a consistent format and reduce merge conflicts.

### Adding to the `.pre-commit-config.yaml` file

```yaml
# .pre-commit-config.yaml
# -----------------------
repos:
# ...
  - repo: https://github.com/jimustafa/sort-gitfile
    rev: v0.0.0
    hooks:
      - id: sort-gitattributes
      - id: sort-gitignore
# ...
```
It is common for the patterns to be separated and organized into blocks,
  with each block corresponding to a category of file types.
Typically, the blocks are separated by blank lines and accompanied by comments indicating the purpose of the block.
For example,
  separate blocks in a `.gitignore` file for the object files and executable files in a `C` project (see [here][1]),
  or separate blocks in a `.gitattributes` file for text and binary files (see [here][2]).

[1]: https://github.com/github/gitignore/blob/master/C.gitignore
[2]: https://github.com/alexkaratarakis/gitattributes/blob/master/Python.gitattributes

### Approach

The files are parsed and broken into blocks; different blocks are separated by blanks lines or comments (or both)
  and sorting of the lines is done within each block (the order of the blocks is preserved).

The sorting must be done carefully since it is possible for a file to match more than one pattern.
In a `gitattributes` file, the attributes that are set for a file matching a pattern can be overridden if the file matches a subsequent pattern;
  clearly, sorting the lines in this case may not yield the same result.
Something similar happens with `gitignore` files when using `!` to negate *prior* ignore patterns to exempt some files from exclusion;
  again, reordering these lines may yield a different set of ignored files.
To deal with this issue, each block is sorted only if it (and the file as a whole) meets some specific criteria;
  basically, all patterns within a block must be mutually exclusive (ie, any given file path can match only one of the patterns) and the behavior of the blocks are independent of each other.
Determining if any two regular expressions can match the same string is a difficult problem and is discussed elsewhere.
Fortunately, with appropriately chosen constraints, it is possible to reorder the lines in both `gitignore` and `gitattributes` without changing how `git` will treat any of the files matching the patterns therein.

In the case of `gitignore`, a file is either ignored, or it is not.
If a file matches a non-negated (with `!`) pattern,
  it is ignored regardless of it matching some other pattern, as long as the file contains no negated patterns;
  any permutation of the patterns in a `gitignore` file will yield the same behavior in the absence of negated patterns.
Hence, the only constraint for sorting `gitignore` files is that they do not have negated patterns.

The case of `gitattributes` files is a quite different since the behavior there is not a binary classification of files;
  here, a multitude of attributes can be assigned to files and overridden depending on the order of the patterns.
Again, there are some conditions (consistent with typical use), that allow for reordering,
  specifically, that each pattern can only contain a single `*` wildcard character, and no others.
This way, it is clear that no two patterns will match the same file,
  and attributes can be assigned without overriding.
Avoiding the overriding of attributes is probably a better practice anyways.

With these abovementioned conditions,
  the lines in both `gitignore` and `gitattributes` files can be freely permuted without changing how files are ignored or the attributes assigned to them.
