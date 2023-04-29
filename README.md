# zwspy

Convert and run Python files with nonstandard indentation characters, including invisible ones.

| Full name | Unicode escape |
| --------- | -------------- |
| ZERO WIDTH JOINER | `\u200d` |
| EN SPACE | `\u2002` |
| SIX-PER-EM SPACE | `\u2006` |
| EM QUAD | `\u2001` |
| IDEOGRAPHIC SPACE | `\u3000` |
| THIN SPACE | `\u2009` |
| THREE-PER-EM SPACE | `\u2004` |
| FIGURE SPACE | `\u2007` |
| PUNCTUATION SPACE | `\u2008` |
| ZERO WIDTH NON-JOINER | `\u200c` |
| NO-BREAK SPACE | `\u00a0` |
| ZERO WIDTH SPACE | `\u200b` |
| NARROW NO-BREAK SPACE | `\u202f` |
| WORD JOINER | `\u2060` |
| FOUR-PER-EM SPACE | `\u2005` |
| MEDIUM MATHEMATICAL SPACE | `\u205f` |
| EN QUAD | `\u2000` |
| EM SPACE | `\u2003` |

## Usage

From the command line:

```
$ python -m zwspy --help
usage: zwspy [-h]
             [--char {...}]
             {run,convert,restore} file

Convert and run Python files with nonstandard indentation characters

positional arguments:
  {run,convert,restore} Run a Python file with nonstandard indentation, convert from a regular file indented with tabs or spaces, or restore from a file with any indentation back to four spaces
  file                  Path to input file

optional arguments:
  -h, --help            show this help message and exit
  --char {...}          Unicode full name of target character for conversion, default ZERO WIDTH SPACE
```

Alternatively, by prepending a special encoding cookie ([PEP-263](https://peps.python.org/pep-0263)) to any file, the Python interpreter will be able to execute it like any other script with normal indentation.

```
# coding=zwspy
```

or

```
# -*- coding: zwspy -*-
```

## Example

```py
# coding=zwspy
from ast import NodeVisitor
class NodeTransformer(NodeVisitor):
​def generic_visit(self, node):
​​for field, old_value in iter_fields(node):
​​​if isinstance(old_value, list):
​​​​new_values = []
​​​​for value in old_value:
​​​​​if isinstance(value, AST):
​​​​​​value = self.visit(value)
​​​​​​if value is None:
​​​​​​​continue
​​​​​​elif not isinstance(value, AST):
​​​​​​​new_values.extend(value)
​​​​​​​continue
​​​​​new_values.append(value)
​​​​old_value[:] = new_values
​​​elif isinstance(old_value, AST):
​​​​new_node = self.visit(old_value)
​​​​if new_node is None:
​​​​​delattr(node, field)
​​​​else:
​​​​​setattr(node, field, new_node)
​​return node
```
