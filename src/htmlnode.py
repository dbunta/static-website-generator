from textnode import *

class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedException()

    def props_to_html(self):
        return f" {" ".join(list(map(lambda x: f"{x[0]}=\"{x[1]}\"",self.props.items())))}"

    def __repr__(selef):
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"children: {self.children}")
        print(f"props: {self.props}")


