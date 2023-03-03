import json


class JSONReader(object):
    def __init__(self, key):
        self.result = ""
        self.brackets = 0  # first bracket is skipped?
        self.key = key

    def parse_line(self, string):
        formatted = string.replace(
            '(', '[').replace(')', ']').replace('PoolStringArray', '')

        self.result += formatted

        self.brackets += string.count('{')
        self.brackets -= string.count('}')

        if self.brackets == 0:
            return string[string.rfind('}') + 1:]

        return None

    def _finditem(self, obj, key):
        result = []
        for k, v in obj.items():
            if k == key:
                result.append(v)
            elif isinstance(v, dict):
                result.extend(self._finditem(v, key))
        return result

    def get_result(self):
        result = json.loads(self.result)
        return self._finditem(result, self.key)
