# Path following algorithm (Code challange)

[![Travis branch](https://img.shields.io/travis/dinoperovic/path-following-algorithm-code-challange/master.svg)](https://travis-ci.org/dinoperovic/path-following-algorithm-code-challange)
[![Codecov](https://img.shields.io/codecov/c/github/dinoperovic/path-following-algorithm-code-challange.svg)](http://codecov.io/github/dinoperovic/path-following-algorithm-code-challange)

Path following algorithm in ASCII Map.

This script requires **Python** `3.4` or higher.

## How to use

Script can be used by either specifying the paths to files, or passing the
input directly.

```sh
$ python follow_path.py examples/map1.txt
Letters: "ACB"
Path as characters: "@---A---+|C|+---+|+-B-x"

$ python follow_path.py examples/map1.txt examples/map2.txt
Letters: "ACB"
Path as characters: "@---A---+|C|+---+|+-B-x"
Letters: "ABCD"
Path as characters: "@|A+---B--+|+----C|-||+---D--+|x"

$ cat examples/map3.txt | python follow_path.py
Letters: "BEEFCAKE"
Path as characters: "@---+B||E--+|E|+--F--+|C|||A--|-----K|||+--E--Ex"
```

### Usage from Python

To use from Python you can use the `FollowPath` class or a shorthand function
`follow_path` that returns values in `(letters, characters)` tuple format.

```python
from follow_path import FollowPath, follow_path

MAP = """
  @---+
      B
K-----|--A
|     |  |
|  +--E  |
|  |     |
+--E--Ex C
   |     |
   +--F--+
"""

path = FollowPath(MAP)
path.run()
print(path.letters)
print(path.characters)

# Shorthand version
path = follow_path(MAP)
print(path[0])
print(path[1])
```

Both will output:

```sh
"BEEFCAKE"
"@---+B||E--+|E|+--F--+|C|||A--|-----K|||+--E--Ex"
```

#### Base logic explained

This script takes an ASCII map input formated like so:
```
@
| C----+
A |    |
+---B--+
  |      x
  |      |
  +---D--+
```

Starting at `@` symbol, it follows the path while extracting uppercase letters
as well as storing all the characters on the way. `x` symbol designates the end
of path, while `+` sing is recognized as corner indicator. Uppercase letters
can also indicate a corner and the same letter crossed more than once
won't be saved as part of extracted letters.

### Tests

Tests can be run with:

```sh
python tests.py
```

