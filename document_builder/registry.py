from pathlib import Path

from document_builder.citizenship.layout import build_citizenship
from document_builder.laalpurja.layout import build_laalpurja


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
}
