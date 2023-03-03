import json

class JSONReader(object):
    def __init__(self, lineno, key):
        self.result = ""
        self.brackets = 1 # first bracket is skipped?
        self.lineno = lineno
        self.key = key
    
    def parse_line(self, string):
        formatted = string.replace('(', '[').replace(')', ']').replace('PoolStringArray', '')

        self.result += formatted
        self.lineno += 1

        self.brackets += string.count('{')
        self.brackets -= string.count('}')

        if self.brackets == 0:
            return string[string.rfind('}') + 1:]

        return None

    def _finditem(self, obj, key, result):
        for k, v in obj.items():
            if k == key:
                result.append(v)
            elif isinstance(v,dict):
                result.extend(self._finditem(v, key, result))
        return result

    def get_result(self):
        result = json.loads("{" + self.result)
        found = self._finditem(result, self.key, [])
        return [(x, self.lineno) for x in found]

