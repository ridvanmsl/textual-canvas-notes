from datetime import datetime

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import MouseDown, MouseMove, MouseUp
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Label, ListItem, ListView

import db
from canvas import Canvas
from modals import RenameModal


class NoteApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 30;
        background: $panel;
        border-right: solid $accent;
    }

    #main_area {
        width: 1fr;
    }

    Canvas {
        width: 100%;
        height: 1fr;
        border: solid $primary;
    }

    .button_row {
        height: auto;
        margin-bottom: 1;
    }

    #note_header_row {
        height: 3;
        layout: horizontal;
    }

    #note_header {
        width: 1fr;
        content-align: center middle;
        background: $accent;
        color: $text;
    }

    #save_note {
        width: 10;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    current_note_id: reactive[int | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Vertical(
                    Button("New Note", id="new_note"),
                    Button("Rename Note", id="rename_note"),
                    Button("Delete Note", id="delete_note"),
                    classes="button_row",
                )
                yield ListView(id="notes_list")
            with Vertical(id="main_area"):
                with Horizontal(id="note_header_row"):
                    yield Label("Select or create a note", id="note_header")
                    yield Button("Save", id="save_note", variant="primary")
                yield Canvas(id="canvas")
        yield Footer()

    def on_mount(self) -> None:
        db.init_db()
        self._refresh_list()

    # ------------------------------------------------------------------ #
    # Mouse passthrough helpers to prevent terminal selection interference
    # ------------------------------------------------------------------ #

    def on_mouse_down(self, event: MouseDown) -> None:
        if isinstance(event.widget, Canvas):
            event.prevent_default()
            event.stop()

    def on_mouse_move(self, event: MouseMove) -> None:
        if self.query_one("#canvas", Canvas).drawing:
            event.prevent_default()
            event.stop()

    def on_mouse_up(self, event: MouseUp) -> None:
        if self.query_one("#canvas", Canvas).drawing:
            event.prevent_default()
            event.stop()

    # ------------------------------------------------------------------ #
    # Note list
    # ------------------------------------------------------------------ #

    def _refresh_list(self) -> None:
        list_view = self.query_one("#notes_list", ListView)
        list_view.clear()
        for note_id, name in db.get_notes():
            item = ListItem(Label(name))
            item.note_id = note_id
            list_view.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item:
            self._load_note(event.item.note_id)

    # ------------------------------------------------------------------ #
    # Load / save
    # ------------------------------------------------------------------ #

    def _load_note(self, note_id: int) -> None:
        self.current_note_id = note_id
        note = db.get_note(note_id)
        if note:
            name, canvas_data = note
            self.query_one("#note_header", Label).update(f"Editing: {name}")
            self.query_one("#canvas", Canvas).load_data(canvas_data or "")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        handlers = {
            "new_note": self._create_note,
            "save_note": self._save_note,
            "delete_note": self._delete_note,
            "rename_note": self._rename_note,
        }
        handler = handlers.get(event.button.id)
        if handler:
            handler()

    def _create_note(self) -> None:
        name = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        note_id = db.create_note(name)
        self._refresh_list()
        self._load_note(note_id)

    def _save_note(self) -> None:
        if self.current_note_id is None:
            return
        canvas = self.query_one("#canvas", Canvas)
        db.save_note(self.current_note_id, canvas.get_data_str())
        self._refresh_list()
        self.notify("Note saved!")

    def _delete_note(self) -> None:
        if self.current_note_id is None:
            return
        db.delete_note(self.current_note_id)
        self.current_note_id = None
        self.query_one("#note_header", Label).update("Select or create a note")
        self.query_one("#canvas", Canvas).load_data("")
        self._refresh_list()

    def _rename_note(self) -> None:
        if self.current_note_id is None:
            return
        note = db.get_note(self.current_note_id)
        if not note:
            return
        old_name = note[0]

        def handle_rename(new_name: str | None) -> None:
            if new_name and new_name.strip():
                db.rename_note(self.current_note_id, new_name.strip())
                self._refresh_list()
                self._load_note(self.current_note_id)

        self.push_screen(RenameModal(old_name), handle_rename)
