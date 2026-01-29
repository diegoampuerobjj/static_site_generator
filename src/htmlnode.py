from typing import Optional

class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[object] = None,
        children: Optional[list] = None,
        props: Optional[dict] = None,
    ):
        """
        Initialize an HTMLNode.
        
        Args:
            tag: HTML tag name (e.g., 'div', 'p')
            value: Text content of the node
            children: List of child HTMLNode objects
            props: Dictionary of HTML attributes
        """

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})" 
        
class LeafNode(HTMLNode):

    def __init__(
        self,
        tag: str,
        value: object,
        props: Optional[dict] = None,
    ):

        """
        Initializze an Leaf Node.
        should differ slightly from the HTMLNode class because:
        
        Args:
            tag: is required even default value is set to None
            value: is required even devault value is set to None
            props: remains optional
        """

        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})" 
    

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: Optional[dict] = None,
    ):

        """
        Initialize an ParentNode.
        This is the opposite to LeafNode.
        
        Args:
            tag: is not optional.
            children: is not optional 
            props: Optional dictionary of HTML attributes
        """

        super().__init__(tag, None, children, props)
    

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        
        c_to_html = ""
        for c in self.children:
            c_to_html += f"{c.to_html()}"
            
        return f"<{self.tag}{self.props_to_html()}>{c_to_html}</{self.tag}>"