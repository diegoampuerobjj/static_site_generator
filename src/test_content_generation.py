import unittest
from content_generation import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        example = """
# Hola
Me llamo diego
"""
        expected = "Hola"
        actual = extract_title(example)
        
        self.assertEqual(expected, actual)

    def test_multiple_heading_title(self):
        example = """
# Hola
## Soy diego de nuevo
Me llamo diego
"""
        expected = "Hola"
        actual = extract_title(example)
        
        self.assertEqual(expected, actual)

    def test_extract_title_raises_without_h1(self):
        markdown = "no title here\njust some text"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()