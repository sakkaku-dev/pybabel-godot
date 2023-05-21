from src.reader.string_reader import StringReader

class ArrayReader(object):
    def __init__(self):
        self.result = []
        self.string = None

    def parse_line(self, string):
        if self.string is not None:
            remainder = self.string.parse_line(string)
            if remainder is None:
                return None
            self.result.extend(self.string.get_result())
            string = remainder
            self.string = None

        i = 0
        while i < len(string):
            c = string[i]
            if c == ']':
                return string[i + 1:]
            elif c == '"':
                self.string = StringReader()
                remainder = self.string.parse_line(string[i + 1:])
                if remainder is None:
                    return None
                else:
                    self.result.extend(self.string.get_result())
                    string = remainder
                    self.string = None
                    i = 0
            else:
                i = i + 1

        raise ValueError("Unterminated array")

    def get_result(self):
        return self.result
