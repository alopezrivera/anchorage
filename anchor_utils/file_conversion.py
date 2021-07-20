import re
import lz4.block


def JSONLZ4_parser(path):
    stream = open(path, 'rb')
    stream.read(8)                  # Skip b"mozLz40\0" header
    string = lz4.block.decompress(stream.read()).decode('utf-8')
    string = re.sub('title', 'name', string)
    string = re.sub('uri', 'url', string)
    return string
