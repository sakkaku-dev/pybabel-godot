from src.reader.json_reader import JSONReader
from src.reader.array_reader import ArrayReader
from src.reader.string_reader import StringReader
from src.keyword_matcher import KeywordMatcher

__version__ = '1.2'


def extract_godot_scene(fileobj, keywords, comment_tags, options):
    """Extract messages from Godot scene files (.tscn).

    :param fileobj: the seekable, file-like object the messages should be
                    extracted from
    :param keywords: a list of property names that should be localized, in the
                     format '<NodeType>/<name>' or '<name>' (example:
                     'Label/text')
    :param comment_tags: a list of translator tags to search for and include
                         in the results (ignored)
    :param options: a dictionary of additional options (optional)
    :rtype: iterator
    """
    encoding = options.get('encoding', 'utf-8')

    matcher = KeywordMatcher(keywords)
    current_value = keyword = None

    for lineno, line in enumerate(fileobj, start=1):
        line = line.decode(encoding)

        if current_value:
            remainder = current_value.parse_line(line)
            if remainder is None:  # Still un-terminated
                pass
            elif remainder.strip():
                raise ValueError("Trailing data after string")
            else:
                for value in current_value.get_result():
                    yield (
                        lineno,
                        keyword,
                        [value],
                        [],
                    )
                current_value = None
            continue

        keyword, value = matcher.parse_and_match(line)
        if keyword:
            if value[0:1] == '[':
                current_value = ArrayReader()
            else:
                current_value = StringReader()
            remainder = current_value.parse_line(value[1:])
            if remainder is None:
                pass  # Un-terminated string
            elif not remainder.strip():
                for value in current_value.get_result():
                    yield (lineno, keyword, [value], [])
                current_value = None
            else:
                raise ValueError("Trailing data after string")


def extract_godot_resource(fileobj, keywords, comment_tags, options):
    """Extract messages from Godot resource files (.res, .tres).

    :param fileobj: the seekable, file-like object the messages should be
                    extracted from
    :param keywords: a list of property names that should be localized, in the
                     format 'Resource/<name>' or '<name>' (example:
                     'Resource/text')
    :param comment_tags: a list of translator tags to search for and include
                         in the results (ignored)
    :param options: a dictionary of additional options (optional)
    :rtype: iterator
    """
    encoding = options.get('encoding', 'utf-8')
    matcher = KeywordMatcher(keywords)
    current_value = keyword = None

    for lineno, line in enumerate(fileobj, start=1):
        line = line.decode(encoding)

        if current_value:
            remainder = current_value.parse_line(line)
            if remainder is None:
                pass  # Still un-terminated
            elif remainder.strip():
                raise ValueError("Trailing data after string")
            else:
                for value in current_value.get_result():
                    yield (
                        lineno,
                        keyword,
                        [value],
                        [],
                    )
                current_value = None
            continue

        if line.startswith('['):
            continue

        keyword, value = matcher.parse_and_match_property(line)
        if keyword:
            if value[0:1] == '[':
                current_value = ArrayReader()
            elif value[0:1] == '{':
                json_key = keyword[keyword.rfind('/') + 1:]
                current_value = JSONReader(json_key)
                current_value.parse_line("{")
            else:
                current_value = StringReader()
            remainder = current_value.parse_line(value[1:])
            if remainder is None:
                pass  # Un-terminated string
            elif not remainder.strip():
                for value in current_value.get_result():
                    yield (lineno, keyword, [value], [])
                current_value = None
            else:
                raise ValueError("Trailing data after string")
