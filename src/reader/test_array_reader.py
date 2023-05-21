from unittest import TestCase, main
from array_reader import ArrayReader


class TestArrayReader(TestCase):
    def test_parse_array(self):
        reader = ArrayReader()
        reader.parse_line('["Hello", "World"]')
        self.assertEqual(reader.get_result(), ["Hello", "World"])


if __name__ == '__main__':
    main()
