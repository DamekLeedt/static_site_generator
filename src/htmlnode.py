class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            raise ValueError()
        return " ".join([f'{item}="{self.props[item]}"' for item in self.props])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}{", " + self.props_to_html() if self.props else ""})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError(self)
        return f"<{self.tag}{f" {super().props_to_html()}" if self.props else ""}>{self.value}</{self.tag}>" if self.tag else self.value
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise Exception("No tag.")
        if not self.children:
            raise Exception("No children.")
        prop_list = []
        for child in self.children:
            prop_list.append(child.to_html())
        return f"<{self.tag}{f" {super().props_to_html()}" if self.props else ""}>{"".join(prop_list)}</{self.tag}>"