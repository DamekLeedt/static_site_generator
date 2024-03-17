class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type}{", " + str(self.url) if self.url else ""})"