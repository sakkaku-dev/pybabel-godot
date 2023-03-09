import re

_godot_node = re.compile(r'^\[node name="([^"]+)" (?:type="([^"]+)")?')
_godot_property_str = re.compile(
    r'^([A-Za-z0-9_/]+)\s*=\s*([\["\{}].+)\Z',
    re.DOTALL,
)

_godot_valid_str = re.compile(r'.*[A-Za-z]+.*')
_godot_special_ignore = re.compile(r'^[_]+.*[_]+$')

NODE_SEPARATOR = '#'


class KeywordMatcher:
    def __init__(self, keywords) -> None:
        self.current_node = None
        self.properties_to_translate = {}

        for keyword in keywords:
            if NODE_SEPARATOR in keyword:
                self.properties_to_translate[tuple(
                    keyword.split(NODE_SEPARATOR, 1))] = keyword
            else:
                self.properties_to_translate[(None, keyword)] = keyword

    def _check_translate_property(self, property):
        for node, keyword in self.properties_to_translate:
            if node == self.current_node or node == None:
                if self._match_property_and_keyword(property, keyword):
                    return self.properties_to_translate[(node, keyword)]
        return None

    def _match_property_and_keyword(self, prop, keyword):
        if keyword.startswith('*'):
            return prop.endswith(keyword[1:])

        if keyword.endswith('*'):
            return prop.startswith(keyword[:-1])

        return prop == keyword

    def parse_and_match_with_node(self, line: str) -> tuple[str]:
        match = _godot_node.match(line)
        if match:
            # Store which kind of node we're in
            node = match.group(2)
            # Instanced packed scenes don't have the type field,
            # change current_node_type to empty string
            self.current_node = node if node is not None else ""
        elif line.startswith('['):
            # We're no longer in a node
            self.current_node = None
        elif self.current_node is not None:
            return self.parse_and_match_property(line)

        return None, None

    def parse_and_match_property(self, line: str) -> tuple[str]:
        match = _godot_property_str.match(line)
        if match:
            property = match.group(1)
            value = match.group(2)

            if self._is_valid_string_value(value):
                keyword = self._check_translate_property(property)
                if keyword:
                    return keyword, value
        return None, None

    def _is_valid_string_value(self, value):
        valid = _godot_valid_str.match(value)
        if valid:
            return not _godot_special_ignore.match(value.replace('"', ''))
        return False
