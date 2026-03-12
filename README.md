# Textual Canvas Notes

A terminal-based note-taking app with a freehand drawing canvas, built with [Textual](https://github.com/Textualize/textual) and SQLite.

## Features

- Create, rename, and delete notes
- Freehand pixel drawing directly inside the terminal
- Notes are persisted in a local SQLite database
- Keyboard-driven UI with mouse drawing support

## Requirements

- Python 3.11+
- [Textual](https://github.com/Textualize/textual) `>= 0.82.0`

## Installation

```bash
git clone https://github.com/ridvanmsl/textual-canvas-notes.git
cd textual-canvas-notes
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

| Action        | How                                      |
|---------------|------------------------------------------|
| New note      | Click **New Note** in the sidebar        |
| Draw          | Hold left mouse button and drag on canvas |
| Save          | Click **Save** or press the button       |
| Rename        | Click **Rename Note**                    |
| Delete        | Click **Delete Note**                    |
| Quit          | Press `q`                                |

## Project Structure

```
textual-canvas-notes/
├── main.py          # Entry point
├── app.py           # Main Textual application
├── canvas.py        # Drawable canvas widget
├── modals.py        # Rename dialog screen
├── db.py            # SQLite database helpers
├── requirements.txt
└── .gitignore
```

## License

MIT
