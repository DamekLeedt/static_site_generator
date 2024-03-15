class TextNode():
    def __init__(self, text, text_type, url="https://www.google.com"):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"