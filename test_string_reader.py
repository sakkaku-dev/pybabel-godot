from unittest import TestCase, main
from babel_godot import StringReader


class TestStringReader(TestCase):
    def test_join_lines(self):
        reader = StringReader()
        reader.parse_line('Hello ')
        reader.parse_line('World')
        self.assertEqual(reader.get_result(), ["Hello World"])


    def test_join_lines_with_windows_line_ending(self):
        reader = StringReader()
        reader.parse_line('Hello \r\n')
        reader.parse_line('World')
        self.assertEqual(reader.get_result(), ["Hello \r\nWorld"])


    def test_join_lines_with_linux_line_ending(self):
        reader = StringReader()
        reader.parse_line('Hello \n')
        reader.parse_line('World')
        self.assertEqual(reader.get_result(), ["Hello \nWorld"])

    def test_join_lines_with_tab(self):
        reader = StringReader()
        reader.parse_line('Hello \t World')
        self.assertEqual(reader.get_result(), ["Hello \t World"])

    def test_end_line_on_double_quotes(self):
        reader = StringReader()
        reader.parse_line('Hello" World')
        self.assertEqual(reader.get_result(), ["Hello"])


if __name__ == '__main__':
    main()
