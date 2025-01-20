from htmlnode import *

class LeafNode(HtmlNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("leaf node missing value")
        if self.tag == None:
            return str(self.value)
        retval = f"<{self.tag}"
        if self.props != None:
            for key,value in self.props.items():
                retval += f" {key}=\"{value}\""
        retval += f">{self.value}</{self.tag}>"
        return retval
