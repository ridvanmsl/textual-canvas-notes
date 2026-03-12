from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class RenameModal(ModalScreen[str]):
    """A modal dialog that prompts the user to rename a note."""

    CSS = """
    #rename_modal {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1 3 3;
        padding: 0 1;
        width: 40;
        height: 11;
        border: thick $background 80%;
        background: $surface;
        align: center middle;
    }

    #rename_modal Label {
        column-span: 2;
        height: 1;
        content-align: center middle;
        width: 100%;
    }

    #rename_modal Input {
        column-span: 2;
    }

    #rename_modal Button {
        width: 100%;
    }
    """

    def __init__(self, old_name: str):
        super().__init__()
        self.old_name = old_name

    def compose(self) -> ComposeResult:
        with Grid(id="rename_modal"):
            yield Label("Rename Note:")
            yield Input(value=self.old_name, id="new_name_input")
            yield Button("OK", id="ok_button", variant="primary")
            yield Button("Cancel", id="cancel_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok_button":
            self.dismiss(self.query_one("#new_name_input", Input).value)
        else:
            self.dismiss(None)
