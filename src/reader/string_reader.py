class StringReader(object):
    def __init__(self):
        self.result = []

    def parse_line(self, string):
        escaped = False
        for i, c in enumerate(string):
            if escaped:
                if c == '\\':
                    self.result.append('\\')
                elif c == 'n':
                    self.result.append('\n')
                elif c == 't':
                    self.result.append('\t')
                else:
                    self.result.append(c)
                escaped = False
            else:
                if c == '\\':
                    escaped = True
                elif c == '"':
                    return string[i + 1:]
                else:
                    self.result.append(c)
        return None

    def get_result(self):
        return [''.join(self.result)]
