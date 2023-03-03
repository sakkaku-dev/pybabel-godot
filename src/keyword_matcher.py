import re

_godot_node = re.compile(r'^\[node name="([^"]+)" (?:type="([^"]+)")?')
_godot_property_str = re.compile(
    r'^([A-Za-z0-9_]+)\s*=\s*([\["\{}].+)\Z',
    re.DOTALL,
)


class KeywordMatcher:
    def __init__(self, keywords) -> None:
        self.current_node = None
        self.properties_to_translate = {}

        for keyword in keywords:
            if '/' in keyword:
                self.properties_to_translate[tuple(
                    keyword.split('/', 1))] = keyword
            else:
                self.properties_to_translate[(None, keyword)] = keyword

    def check_translate_property(self, property):
        keyword = self.properties_to_translate.get(
            (self.current_node, property))
        if keyword is None:
            keyword = self.properties_to_translate.get((None, property))
        return keyword

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
            keyword = self.check_translate_property(property)
            if keyword:
                return keyword, value
        return None, None
