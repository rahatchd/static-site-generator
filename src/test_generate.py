import unittest

from generate import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# title"), "title")

    def test_extract_title_whitespace(self):
        self.assertEqual(extract_title("#   title  "), "title")

    def test_extract_title_multiline(self):
        doc = """

# title

- so basically a bunch of
- items in a list
"""
        self.assertEqual(extract_title(doc), "title")

    def test_extract_title_first(self):
        doc = """

# title

# another one
"""
        self.assertEqual(extract_title(doc), "title")

    def test_extract_title_invalid_raises(self):
        with self.assertRaises(ValueError):
            _ = extract_title("ain't no title long enough")
