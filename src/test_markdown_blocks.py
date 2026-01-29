import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBLockType(unittest.TestCase):
        def test_block_to_block_types(self):
            md = """
# Este es el Titulo

This is **bolded** paragraph

> This is quote with another paragraph with _italic_ text and `code` here
> This is the same quote but with paragraph on a new line

```
def this_is_a_function(text):
    print(text)
```

- This is a list
- with items

This is another paragraph

1. ordered first
2. ordered second
3. ordered third
"""
            blocks = markdown_to_blocks(md)
            heading = block_to_block_type(blocks[0])
            paragraph = block_to_block_type(blocks[1])
            quote = block_to_block_type(blocks[2])
            multiline_code = block_to_block_type(blocks[3])
            unordered_list = block_to_block_type(blocks[4])
            ordered_list = block_to_block_type(blocks[6])
            
            self.assertEqual(heading, BlockType.HEADING)
            self.assertEqual(paragraph, BlockType.PARAGRAPH)
            self.assertEqual(quote, BlockType.QUOTE)
            self.assertEqual(multiline_code, BlockType.CODE)
            self.assertEqual(unordered_list, BlockType.UNORDERED_LIST)
            self.assertEqual(ordered_list, BlockType.ORDERED_LIST)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
# This is heading 1
## This is heading 2

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is heading 1</h1><h2>This is heading 2</h2><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is quote with another paragraph with italic text and code here
> This is the same quote but with paragraph on a new line

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is quote with another paragraph with italic text and code here This is the same quote but with paragraph on a new line</blockquote></div>",
        )
    
    def test_unorderedblock(self):
        md = """
- This is quote with another paragraph with italic text and code here
- This is the same quote but with paragraph on a new line
- This is more text
- And this is more text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is quote with another paragraph with italic text and code here</li><li>This is the same quote but with paragraph on a new line</li><li>This is more text</li><li>And this is more text</li></ul></div>",
        )

    def test_orderedblock(self):
        md = """
1. This is quote with another paragraph with italic text and code here
2. This is the same quote but with paragraph on a new line
3. This is more text
4. And this is more text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is quote with another paragraph with italic text and code here</li><li>This is the same quote but with paragraph on a new line</li><li>This is more text</li><li>And this is more text</li></ol></div>",
        )   

if __name__ == "__main__":
    unittest.main() 