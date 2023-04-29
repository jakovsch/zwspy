import argparse, os, runpy
from zwspy import wsnames, encodestr, decodestr

args = argparse.ArgumentParser(
    prog='zwspy',
    description='Convert and run Python files with nonstandard indentation characters',
)
args.add_argument(
    'action',
    choices=['run', 'convert', 'restore'],
    help='Run a Python file with nonstandard indentation, ' \
        'convert from a regular file indented with tabs or spaces, ' \
        'or restore from a file with any indentation back to four spaces',
)
args.add_argument(
    'file',
    help='Path to input file',
)
args.add_argument(
    '--char',
    required=False,
    default='ZERO WIDTH SPACE',
    choices=list(wsnames.keys()),
    help='Unicode full name of target character for conversion, default ZERO WIDTH SPACE',
)

def _get_code_from_file(_, fname):
    import io
    with io.open_code(fname) as f:
        t = io.TextIOWrapper(f, encoding='utf-8')
        code = compile(
            ''.join(decodestr(t.readline)),
            fname, 'exec',
        )
    return code, fname
runpy._get_code_from_file = _get_code_from_file

args = args.parse_args()
action = args.action
file = os.path.abspath(os.fsdecode(args.file))
char = args.char
out = None

with open(file, 'r+', encoding='utf-8') as f:
    if action == 'run':
        runpy.run_path(file)
    elif action == 'convert':
        out = ''.join(encodestr(f.readline, char=char))
    elif action == 'restore':
        out = ''.join(decodestr(f.readline))
    if out:
        f.seek(0)
        f.write(out)
        f.truncate()
