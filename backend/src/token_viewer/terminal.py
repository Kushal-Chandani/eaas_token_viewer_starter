"""Simple terminal view that calls the same controller as the web page."""

from __future__ import annotations

import json
from pathlib import Path

from token_viewer.controller import CommandError
from token_viewer.wiring import build_controller
from token_viewer.view_models import Message


def main() -> None:
    """Run a small command loop until the user enters quit."""
    controller = build_controller()
    print(
        "Token viewer terminal. Commands: load REPOSITORY REVISION, messages JSON, capture PATH, view KEY, select INDEX, show, quit"
    )
    _show(controller.view_model())
    while True:
        try:
            line = input("token-viewer> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not line:
            continue
        command, _, argument = line.partition(" ")
        try:
            if command in {"quit", "exit"}:
                return
            if command == "show":
                result = controller.view_model()
            elif command == "load":
                repository, separator, revision = argument.partition(" ")
                if not separator:
                    raise CommandError("Usage: load OWNER/REPOSITORY REVISION")
                result = controller.load_model(repository, revision)
            elif command == "messages":
                parsed = json.loads(argument)
                messages = [Message.model_validate(item) for item in parsed]
                result = controller.set_messages(messages)
            elif command == "capture":
                path = Path(argument.strip().strip('"'))
                result = controller.load_capture(
                    path.name, path.read_text(encoding="utf-8")
                )
            elif command == "view":
                result = controller.select_view(argument)
            elif command == "select":
                result = controller.select_token(int(argument))
            else:
                print("Unknown command. Type one of the commands shown at startup.")
                continue
            _show(result)
        except (CommandError, ValueError, OSError, json.JSONDecodeError) as error:
            print(f"Error: {error}")


def _show(view_model: object) -> None:
    """Print the latest view-model in readable JSON."""
    model = getattr(view_model, "model_dump")()
    print(json.dumps(model, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
