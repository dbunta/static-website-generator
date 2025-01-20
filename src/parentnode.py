from htmlnode import *

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node missing tag")
        if self.children == None:
            raise ValueError("parent node missing children")
        
        retval = f"<{self.tag}"
        if self.props != None:
            for k,v in self.props.items():
                retval += f" {k}=\"{v}\""
        retval += ">"

        for child in self.children:
            retval += child.to_html()

        retval += f"</{self.tag}>"

        return retval

