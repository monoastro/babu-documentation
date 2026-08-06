from pathlib import Path

from document_builder.citizenship.layout import build_citizenship
from document_builder.laalpurja.layout import build_laalpurja
from document_builder.letter.layout import build_letter


DOCUMENTS = {
    "citizenship": {
        "builder": build_citizenship,
        "schema": (
            Path(__file__).parent.parent
            / "information_extraction"
            / "schemas"
            / "citizenship.json"
        ),
    },
    "laalpurja": {
        "builder": build_laalpurja,
        "schema": (
            Path(__file__).parent.parent
            / "information_extraction"
            / "schemas"
            / "laalpurja.json"
        ),
    },
    "letter": {
        "builder": build_letter,
        "schema": (
            Path(__file__).parent.parent
            / "information_extraction"
            / "schemas"
            / "letter.json"
        ),
    },
}
