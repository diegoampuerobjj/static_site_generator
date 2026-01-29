import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """Test that text nodes are equal"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        """Test that different text nodes are not equal"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_false_different_type(self):
        """Test that nodes with different types are not equal"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        """Test equality with URLs"""
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_eq_false_different_url(self):
        """Test that nodes with different URLs are not equal"""
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        """"Test equality when URL is None"""
        node = TextNode("Click here", TextType.LINK, None) 
        node2 = TextNode("Click here", TextType.LINK, None)
        self.assertEqual(node, node2)

class TestTextNodeToHTML(unittest.TestCase):
    
    def test_text(self):
        """Test that text node converts successfully to HTML"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        """Test that link node converts successfully to HTML"""
        node = TextNode("Click here", TextType.LINK, "https://umulabs.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(
            html_node.props, 
            {"href": "https://umulabs.com"}
            )

    def test_image(self):
        """Test that image node converts successsfully to HTML"""
        node = TextNode("Image about Jozef Chen", TextType.IMAGE, "https://umulabs.com/jozef_chen.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "https://umulabs.com/jozef_chen.png", "alt": "Image about Jozef Chen"}
            )
        
if __name__ == "__main__":
    unittest.main()