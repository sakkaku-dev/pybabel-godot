from unittest import TestCase, main
from json_reader import JSONReader


class TestJsonReader(TestCase):
    def test_extract_property(self):
        reader = JSONReader("name")
        reader.parse_line('"id": 1, "name": "Bob"}')
        self.assertEqual(reader.get_result(), ["Bob"])

    def test_extract_nested_property(self):
        reader = JSONReader("name")
        reader.parse_line('"id": 1, "data": {"person": {"name": "Bob"}}}')
        self.assertEqual(reader.get_result(), ["Bob"])

    def test_extract_multiple_properties(self):
        reader = JSONReader("name")
        reader.parse_line(
            '"id": 1, "name": "Max", "person": {"name": "Bob"}}')
        self.assertEqual(reader.get_result(), ["Max", "Bob"])

    def test_extract_by_multiple_lines(self):
        reader = JSONReader("name")
        reader.parse_line('"id": 1,')
        reader.parse_line('"name": "Bob"')
        reader.parse_line('}')
        self.assertEqual(reader.get_result(), ["Bob"])


if __name__ == '__main__':
    main()
