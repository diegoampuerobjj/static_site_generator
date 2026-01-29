import unittest

from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes
)

from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_eq(self):
        """Test if all the parameters and outcomes are equal"""
        node = TextNode("hello **world**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
            ]
        
        self.assertEqual(expected, actual)
    
    def test_text_after_bold(self):
        """Test the text coming after the delimeter"""
        node = TextNode("**China** is a great country", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("China", TextType.BOLD),
            TextNode(" is a great country", TextType.TEXT)
            ]

        self.assertEqual(expected, actual)

    def test_code(self):
        """Test the text with code delimiter"""
        node = TextNode("I like to code `hello, world` all the time.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("I like to code ", TextType.TEXT),
            TextNode("hello, world", TextType.CODE),
            TextNode(" all the time.", TextType.TEXT),
            ]

        self.assertEqual(expected, actual)

    def test_italic(self):
        """Test the text with italic delimiter"""
        node = TextNode("This is the _italic_ delimiter.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" delimiter.", TextType.TEXT),
            ]

        self.assertEqual(expected, actual)

    def test_multiple_delimiter(self):
        """Test the text with multiple same delimiter"""
        node = TextNode("This is the **bold**, then we have **another bold**.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is the ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", then we have ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            ]

        self.assertEqual(expected, actual)

    
class TestExtractMarkdown(unittest.TestCase):    
    def test_extract_markdown_images(self):
        """Test if the text contains images"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        "Test if the test contains links"
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_same_link_multiple_times(self):
        "Test the output for the same link multiple times"
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to boot dev", "https://www.boot.dev")], matches)

    def test_same_image_multiple_times(self):
        "Test the output for the same image multiple times"
        matches = extract_markdown_images(
            "Hey guys, what's the difference between ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_link_no_matches(self):
        "Test the link extract function with with no []() patterns"
        matches = extract_markdown_links(
            "This is a simple test, we have no patters at all, so it should be ignored."
        )
        self.assertEqual([], matches)

    def test_image_no_matches(self):
        "Test the image extract function with with no []() patterns"
        matches = extract_markdown_images(
            "This is a simple test, we have no patters at all, so it should be ignored."
        )
        self.assertEqual([], matches)
    
    def test_incomplete_link(self):
        "Test the link extract funcion with incomplete patterns"
        matches = extract_markdown_links(
            "Hey guys! visit my site at [](https://example.com)"
        )
        self.assertEqual([("", "https://example.com")], matches)

    def test_incomplete_image(self):
        "Test the imaged extract funcion with incomplete patterns"
        matches = extract_markdown_images(
            "Hey guys! visit my site at ![](https://example.com/img.png)" 
        )
        self.assertEqual([("", "https://example.com/img.png")], matches)

class TestSplitLinkAndImagesNodes(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode(
            "[boot](https://www.boot.dev)", 
            TextType.TEXT
        )        
        new_nodes = split_nodes_link([node])        
        self.assertListEqual(
            [
                TextNode("boot", TextType.LINK, "https://www.boot.dev")
            ], 
            new_nodes
        )

    def test_single_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)", 
            TextType.TEXT
        )        
        new_nodes = split_nodes_image([node])        
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ], 
            new_nodes
        )

    def test_no_links_but_non_text_present(self):
        node = TextNode("just bold stuff", TextType.BOLD)        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("just bold stuff", TextType.BOLD)
            ], 
            new_nodes
        )
  
    def test_no_image_but_non_text_present(self):
        node = TextNode("just bold stuff", TextType.BOLD)        
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("just bold stuff", TextType.BOLD)
            ], 
            new_nodes
        )             


class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        nodes = text_to_textnodes("hello world")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "hello world")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_bold(self):
        nodes = text_to_textnodes("this is **bold** text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "this is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_italic(self):
        nodes = text_to_textnodes("this is _italic_ text")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "this is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_code(self):
        nodes = text_to_textnodes("run `code()` now")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "run ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "code()")
        self.assertEqual(nodes[1].text_type, TextType.CODE)

        self.assertEqual(nodes[2].text, " now")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_image(self):
        nodes = text_to_textnodes(
            "look ![alt text](https://example.com/img.png) here"
        )
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "look ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "alt text")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.png")
        self.assertEqual(nodes[2].text, " here")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_link(self):
        nodes = text_to_textnodes(
            "click [here](https://example.com) please"
        )
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "click ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "here")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " please")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_mixed(self):
        nodes = text_to_textnodes(
            "this is **bold** and _italic_ with `code`"
        )
        bold_nodes = [n for n in nodes if n.text_type == TextType.BOLD]
        italic_nodes = [n for n in nodes if n.text_type == TextType.ITALIC]
        code_nodes = [n for n in nodes if n.text_type == TextType.CODE]
        
        self.assertEqual(len(bold_nodes), 1)
        self.assertEqual(bold_nodes[0].text, "bold")
        self.assertEqual(len(italic_nodes), 1)
        self.assertEqual(italic_nodes[0].text, "italic")
        self.assertEqual(len(code_nodes), 1)
        self.assertEqual(code_nodes[0].text, "code")
    


if __name__ == "__main__":
    unittest.main()