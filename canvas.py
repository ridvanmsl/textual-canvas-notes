import json

from textual.events import MouseDown, MouseMove, MouseUp
from textual.reactive import reactive
from textual.widgets import Static


class Canvas(Static):
    """A drawable canvas widget that tracks pixel positions as characters."""

    canvas_data: reactive[dict] = reactive({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drawing = False
        self.can_focus = True

    def on_mount(self) -> None:
        self.capture_mouse()

    def on_enter(self) -> None:
        self.capture_mouse()

    def on_leave(self) -> None:
        if not self.drawing:
            self.release_mouse()

    def on_blur(self) -> None:
        self.release_mouse()

    def on_mouse_down(self, event: MouseDown) -> None:
        event.prevent_default()
        event.stop()
        if event.button == 1:
            self.drawing = True
            self.capture_mouse()
            self._draw(event.x, event.y)

    def on_mouse_move(self, event: MouseMove) -> None:
        event.prevent_default()
        event.stop()
        if self.drawing:
            self._draw(event.x, event.y)

    def on_mouse_up(self, event: MouseUp) -> None:
        event.prevent_default()
        event.stop()
        if self.drawing:
            self.drawing = False

    def on_click(self, event: MouseUp) -> None:
        event.prevent_default()
        event.stop()

    def _draw(self, x: int, y: int) -> None:
        self.canvas_data[(x, y)] = "#"
        self.refresh()

    def render(self) -> str:
        if not self.size:
            return ""
        width, height = self.size.width, self.size.height
        lines = []
        for y in range(height):
            line = ""
            for x in range(width):
                line += self.canvas_data.get((x, y), " ")
            lines.append(line)
        return "\n".join(lines)

    def load_data(self, data_str: str) -> None:
        """Deserialize canvas data from a JSON string and refresh the view."""
        if data_str:
            try:
                raw = json.loads(data_str)
                self.canvas_data = {tuple(map(int, k.split(","))): v for k, v in raw.items()}
            except Exception:
                self.canvas_data = {}
        else:
            self.canvas_data = {}
        self.refresh()

    def get_data_str(self) -> str:
        """Serialize canvas data to a JSON string for storage."""
        serializable = {f"{k[0]},{k[1]}": v for k, v in self.canvas_data.items()}
        return json.dumps(serializable)
