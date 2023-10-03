from unittest import TestCase, main
from keyword_matcher import KeywordMatcher


class TestKeywordMatcher(TestCase):

    # Nodes

    def test_match_node_property(self):
        matcher = KeywordMatcher(['Label#text'])
        matcher.parse_and_match_with_node('[node name="Name" type="Label"]')
        _, text = matcher.parse_and_match_with_node('text = "Hello World"')
        self.assertEqual(text, '"Hello World"')

        matcher.parse_and_match_with_node('[node name="Name" type="Control"]')
        _, text = matcher.parse_and_match_with_node('text = "Ignored"')
        self.assertIsNone(text)

    def test_match_any_node_property(self):
        matcher = KeywordMatcher(['text'])
        matcher.parse_and_match_with_node('[node name="Name" type="Label"]')
        _, text = matcher.parse_and_match_with_node('text = "Hello"')
        self.assertEqual(text, '"Hello"')

        matcher.parse_and_match_with_node('[node name="Name" type="Control"]')
        _, text = matcher.parse_and_match_with_node('text = "World"')
        self.assertEqual(text, '"World"')

    def test_match_last_node_property(self):
        matcher = KeywordMatcher(['Label#*/text'])
        matcher.parse_and_match_with_node('[node name="Name" type="Label"]')
        _, text = matcher.parse_and_match_with_node('items/0/text = "Hello"')
        self.assertEqual(text, '"Hello"')

    def test_match_first_node_property(self):
        matcher = KeywordMatcher(['Label#items/*'])
        matcher.parse_and_match_with_node('[node name="Name" type="Label"]')
        _, text = matcher.parse_and_match_with_node('items/0/text = "Hello"')
        self.assertEqual(text, '"Hello"')

    def test_match_property_without_node_type(self):
        matcher = KeywordMatcher(['text'])
        matcher.parse_and_match_with_node('[node name="Name"]')
        _, text = matcher.parse_and_match_with_node('text = "Hello"')
        self.assertEqual(text, '"Hello"')

    # Property

    def test_match_property(self):
        matcher = KeywordMatcher(['text'])
        _, text = matcher.parse_and_match_property('text = "PLAYER_NAME"')
        self.assertEqual(text, '"PLAYER_NAME"')

    def test_match_property_array_type(self):
        matcher = KeywordMatcher(['actions'])
        _, text = matcher.parse_and_match_property(
            'actions = Array[String](["up", "down"])')
        self.assertEqual(text, '["up", "down"]')

    def test_match_last_property_name(self):
        matcher = KeywordMatcher(['*/text'])
        _, text = matcher.parse_and_match_property('items/0/text = "Hello"')
        self.assertEqual(text, '"Hello"')

    def test_match_first_property_name(self):
        matcher = KeywordMatcher(['items/*'])
        _, text = matcher.parse_and_match_property('items/0/text = "Hello"')
        self.assertEqual(text, '"Hello"')

    def test_match_property_name_containing(self):
        matcher = KeywordMatcher(['*/text*'])
        _, text = matcher.parse_and_match_property('items/0/text_1 = "Hello"')
        self.assertEqual(text, '"Hello"')

    def test_match_only_string(self):
        matcher = KeywordMatcher(['text'])
        _, text = matcher.parse_and_match_property('text = 10')
        self.assertIsNone(text)

    def test_do_not_match_value_without_characters(self):
        matcher = KeywordMatcher(['text'])
        _, text = matcher.parse_and_match_property('text = "+"')
        self.assertIsNone(text)

        _, text = matcher.parse_and_match_property('text = ""')
        self.assertIsNone(text)

        _, text = matcher.parse_and_match_property('text = "12345"')
        self.assertIsNone(text)

    def test_ignore_values_with_special_marker(self):
        matcher = KeywordMatcher(['text'])
        _, text = matcher.parse_and_match_property('text = "_ignored_"')
        self.assertIsNone(text)

        _, text = matcher.parse_and_match_property('text = "__ignored__"')
        self.assertIsNone(text)


if __name__ == '__main__':
    main()
