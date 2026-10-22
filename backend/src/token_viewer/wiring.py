"""Which controller the web back end and terminal view use."""

from token_viewer.controller import Controller
from token_viewer.real_controller import TokenViewerController


def build_controller() -> Controller:
    """Return the real tokenizer controller; loading stays lazy until requested."""
    return TokenViewerController()
