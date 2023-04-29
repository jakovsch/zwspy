import codecs, encodings, io
from zwspy.codec.indentreplace import encodestr, decodestr

def encode(input, errors='strict'):
    return ''.join(encodestr(io.StringIO(input).readline)).encode('utf-8', errors), len(input)

def decode(input, errors='strict'):
    return ''.join(decodestr(io.StringIO(input.decode('utf-8', errors)).readline)), len(input)

class IncrementalEncoder(encodings.utf_8.IncrementalEncoder):
    def encode(self, object, final=False):
        self.buffer += object
        if final:
            buffer, self.buffer = self.buffer, ''
            return super().encode(''.join(encodestr(io.StringIO(buffer).readline)), final)
        else: return b''

class IncrementalDecoder(encodings.utf_8.IncrementalDecoder):
    def decode(self, object, final=False):
        self.buffer += object
        if final:
            buffer, self.buffer = self.buffer, b''
            return ''.join(decodestr(io.StringIO(super().decode(buffer, final)).readline))
        else: return ''

class StreamReader(encodings.utf_8.StreamReader):
    decode = decode

class StreamWriter(encodings.utf_8.StreamWriter):
    encode = encode

def search_function(encoding):
    if encoding != 'zwspy': return None
    return codecs.CodecInfo(
        name='zwspy',
        encode=encode,
        decode=decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

codecs.register(search_function)
