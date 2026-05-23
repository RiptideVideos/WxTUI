from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Input, Rule, Label, Checkbox, RadioButton, RadioSet, Digits, Footer, Header, Static, Placeholder
from textual.screen import Screen

class Warning(HorizontalGroup):
    DEFAULT_CSS = "Warning {\nborder: solid grey;\nheight: 5;}"
    def __init__(self, headline, sender, expires, areas, id, **kwargs):
        super().__init__(**kwargs)
        self.headline = headline
        self.sender = sender
        self.expires = expires
        self.areas = areas
        self.id = id

    def compose(self):
        yield Static(f"""{self.headline}\n{self.sender} - Expires: {self.expires}\n{self.areas}""")
        yield Button("Info", id=self.id, variant="default", dock="right")

