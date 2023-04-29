import functools, tokenize, unicodedata

ws = set(
    [
        #'\u0009',
        '\u00A0',
        #'\u180E',
        '\u202F',
        '\u205F',
        '\u2060',
        '\u3000',
        #'\uFEFF',
    ] + [chr(0x2000 + i) for i in range(14)]
)
wsnames = {
    unicodedata.name(i): i for i in ws
}

def _asgen(fn):
    i = fn()
    while i:
        yield i
        i = fn()

def _ascall(it):
    it = iter(it)
    return lambda: next(it)

def indent_replace(line, indent, char):
    #char *= len(indent)
    spl = iter(line.split(indent))
    return ''.join(functools.reduce(
        lambda acc, i: acc + char if not i else acc + indent.join((i, *spl)),
        spl, '',
    ))

def encodestr(readline, char='ZERO WIDTH SPACE'):
    ind = None
    lines = list(_asgen(readline))
    for t in tokenize.generate_tokens(_ascall(lines)):
        if t.type == tokenize.INDENT:
            ind = t.string
            break
    for line in lines:
        if ind and ind in line:
            line = indent_replace(line, ind, wsnames.get(char, ind))
        yield line

def decodestr(readline, char='    '):
    lines = _asgen(readline)
    for line in lines:
        if line[0] in ws:
            line = indent_replace(line, line[0], char)
        yield line
