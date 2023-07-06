from __future__ import annotations


class TextEmbed:
    def __init__(self, start: str = ">>>", end: str = ""):
        self.start = start + " "
        self.end = end
        self.msg = ""


    
    def __str__(self) -> str:
        return self.start + self.msg + self.end

    def __radd__(self, other: str | TextEmbed):
        if isinstance(other, str):
            self.msg = other + self.msg
            return self
        self.msg = other.msg + self.msg
        return self
        

    def __add__(self, other: str | TextEmbed):
        if isinstance(other, str):
            self.msg = self.msg + other
            return self
        self.msg = self.msg + other.msg
        return self

    def __iadd__(self, other: str | TextEmbed):
        if isinstance(other, str):
            self.msg = self.msg + other
            return self
        self.msg = self.msg + other.msg
        return self

    def title(self, msg) -> TextEmbed:
        self.msg += f"# `{msg}`\r\n\n"
        return self

    def description(self, msg) -> TextEmbed:
        self.msg += f"*{msg}*\n"
        return self

    def add_field(self, key, value) -> TextEmbed:
        if value != "":
            self.msg += f"**`{key}`**   *{value}*\n"
        else:
            self.msg += f"**`{key}`**   {value}\n"
        return self

    def add_items(self, key, values, attr: str | None = None) -> TextEmbed:
        self.msg += f"# `{key}`\n"
        if attr is None:
            for val in values:
                if val != "":
                    self.msg += f"*{val}*\n"
                else:
                    self.msg += f"{val}"
        if attr is not None:
            for val in values:
                if hasattr(val, attr):
                    val = getattr(val, attr)
                if val != "":
                    self.msg += f"*{val}*\n"
                else:
                    self.msg += f"{val}"

        return self

    def subheading(self, msg) -> TextEmbed:
        self.msg += f"## `{msg}`\n"
        return self
    
    def add_manual(self, msg) -> TextEmbed:
        self.msg += str(msg)
        return self
