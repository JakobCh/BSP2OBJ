import struct
from ctypes import *

class PAK(object):
    def __init__(self, stream):
        self.stream = stream

        header, = struct.unpack("4s", stream.read(4))

        #Python3 Bytearray to string convertion
        if type(header) == type(b""):
            header = header.decode("utf-8")

        if(header != "PACK"):
            raise ValueError("Expected PACK header, found " + header)
            
        # Get the offset and size of the PAK directory list
        offset, size = struct.unpack('ii', stream.read(8))
        stream.seek(offset)

        FILE_INDEX_SIZE_BYTES = 64
        self.directory = {}
        for i in range(0, int(size / FILE_INDEX_SIZE_BYTES)):
            filename, offset, size = struct.unpack("56sii", stream.read(FILE_INDEX_SIZE_BYTES))
            filename = c_char_p(filename).value # null-terminate string

            #Python3 Bytearray to string convertion
            if type(filename) == type(b""):
                filename = filename.decode("utf-8")

            self.directory[filename] = (offset, size)
