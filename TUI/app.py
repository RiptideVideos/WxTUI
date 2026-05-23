import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Input, Rule, Label, Checkbox, RadioButton, RadioSet, Digits, Footer, Header, Static, Placeholder
from textual.screen import Screen
import pyfiglet
from fetching.data import masterFetch, idFetch
from datetime import datetime

abbreviations = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY"
]
class Warning(HorizontalGroup):
    DEFAULT_CSS="Warning {\nheight: 5;}"
    def __init__(self, headline, sender, expires, areas, buttonClass, **kwargs):
        super().__init__(**kwargs)
        self.headline = headline
        self.sender = sender
        self.expires = expires
        self.areas = areas
        self.buttonClass = buttonClass
            
    def compose(self):
        yield Static(f"""{self.headline}\n{self.sender} - Expires: {self.expires}\n{self.areas}""")
        yield Button("Info", id="info", name=self.buttonClass)

class MemoBlock(HorizontalGroup):
    def __init__(self, headline, desc, instruc, **kwargs):
        super().__init__(**kwargs)
        self.headline = headline
        self.desc = desc
        self.instruc = instruc
    def compose(self):
        yield Static(f"{self.headline}\n\n{self.desc}\n\n{self.instruc}")

class RadioType(HorizontalGroup):
    def compose(self):
        yield RadioButton("All", id="all")
        yield RadioButton("Tornado", id="tornado", value=True,)
        yield RadioButton("Storm/Flood", id = "storm-flood")

    def on_radio_button_changed(self, event: RadioButton.Changed) -> None:
        if event.value:
            for btn in self.query(RadioButton):
                if btn is not event.radio_button:
                    btn.value = False
class RadioSev(HorizontalGroup):
    def compose(self):
        yield Checkbox("Extreme", id="extreme", value=True)
        yield Checkbox("Severe", id = "severe", value=True)
        yield Checkbox("Moderate", id = "moderate", value=True)
class Information(HorizontalGroup):
    def compose(self):
        yield Static("""
Developed by Simon Crystal
Data from: api.weather.gov
Made with Textual""")
        
class Alerts(VerticalScroll):
    DEFAULT_CSS = """Alerts {\nheight: 84vh;\n border: solid white;\nmax-width: 70%;}"""
class Memo(VerticalScroll):
    DEFAULT_CSS = "Memo {\nheight: 84vh;\nborder: solid white;\nmax-width: 30%;}"

class Title(HorizontalGroup):
    def compose(self):
        yield Label(pyfiglet.figlet_format("WxTUI Alpha", font="slant"), id="titleFiglet")
        yield Rule(orientation="vertical", id="whiterule")
        yield Information()
class Settings(HorizontalGroup):
    DEFAULT_CSS = """Settings {\nheight: 5;\nborder: solid white;\nmax-width: 100%;}"""
    def compose(self):
        yield RadioType(id="radiotype")
        yield Input(placeholder="Enter State Code (Ex: NC) | Seperate With Spaces", id="stateinput", type="text")
        yield RadioSev(id="radiosev")

class AlertsAndMemo(HorizontalGroup):
    def compose(self):
        yield Alerts(id="alerts")
        yield Memo(id="memo")


class MyFooter(Placeholder):
    DEFAULT_CSS = """MyFooter {\nheight: 5;\ndock: bottom;}"""

class MainApp(App):

    BINDINGS = []
    CSS_PATH = "title.tcss"

    def compose(self) -> ComposeResult:
        yield Title()
        yield Settings()
        yield AlertsAndMemo()
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "info":
             ID = event.button.name
             self.getId(ID)
    
    def on_mount(self):
        self.getData()
        self.set_interval(15, self.getData)
    
    def getId(self, id):
        data = idFetch(id)

        self.query("#memo > Widget").remove()

        newMemoBlock = MemoBlock(
            headline=data[1],
            desc=data[2],
            instruc=data[3]
        )
        self.query_one("#memo").mount(newMemoBlock)
            
            
    def getData(self):
        moderateSev = self.query_one("#moderate").value
        severeSev = self.query_one("#severe").value
        extremeSev = self.query_one("#extreme").value
        stateCodes = (self.query_one("#stateinput").value).split()

        allAlerts = self.query_one("#all").value
        tornadoAlerts = self.query_one("#tornado").value
        stormfloodAlerts = self.query_one("#storm-flood").value

        toFetch = ""

        def canState(stateCodes):
            if stateCodes == []:
                return False
            for code in stateCodes:
                if not(code in abbreviations):
                    return False
            return True
        if canState(stateCodes):
            toFetch = "state"
        elif allAlerts:
            toFetch = "all"        
        elif tornadoAlerts:
            toFetch = "tornado"
        elif stormfloodAlerts:
            toFetch = "storm/flood"
        
        data = masterFetch(toFetch, stateCodes, extremeSev, severeSev, moderateSev)

        self.query("#alerts > Widget").remove()
        try:
            for alert in data.values():
                headline = alert["headline"]
                event = alert["event"]
                severity = alert["severity"]
                onset = datetime.strptime(alert["onset"],"%Y-%m-%dT%H:%M:%S%z")
                expires = datetime.strptime(alert["expires"],"%Y-%m-%dT%H:%M:%S%z")
                areas = alert["areas"]
                sender = alert["sender"]
                color = alert["color"]
                ID = alert["id"]

                readableExpires = str(expires.month) + "/" + str(expires.day) + " " + str(expires.hour) + ":" + str(expires.minute)
            
                newAlert = Warning(
                    headline=event,
                    sender=sender,
                    expires=readableExpires,
                    areas=areas,
                    classes=color+"Warn",
                    buttonClass=ID
            )
                self.query_one("#alerts").mount(newAlert)
        except Exception as e:
            newAlert = Warning(
                headline="No Warnings of this Type!",
                sender="",
                expires="",
                areas="",
                classes="whiteWarn"
            )
            self.query_one("#alerts").mount(newAlert)



if __name__ == "__main__":
    app = MainApp()
    app.run()