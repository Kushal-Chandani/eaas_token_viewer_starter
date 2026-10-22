"""Real controller connecting API/terminal commands to the tokenizer model."""

from __future__ import annotations

import json
from typing import Any

from token_viewer.controller import CommandError, Controller
from token_viewer.model import TokenizerModel, TokenizerModelError
from token_viewer.view_models import (
    CaptureView,
    Message,
    TokenView,
    TokenizerView,
    ViewModel,
    ViewOption,
)


class TokenViewerController(Controller):
    """Translate view commands into model operations and display data."""

    def __init__(self) -> None:
        self._model = TokenizerModel()

    def view_model(self) -> ViewModel:
        model = self._model
        tokenizer_view = None
        if model.repository is not None and model.revision is not None:
            tokenizer_view = TokenizerView(
                repository=model.repository, revision=model.revision
            )
        view_options = [
            ViewOption(key=key, title=view.title) for key, view in model.views.items()
        ]
        tokens = [
            TokenView(
                index=index,
                id=token.token_id,
                piece=token.piece,
                text=token.text,
                start=token.start,
                end=token.end,
                special=token.special,
            )
            for index, token in enumerate(model.tokens())
        ]
        capture = None
        if model.capture_name is not None:
            capture = CaptureView(
                name=model.capture_name,
                answer=model.capture_answer,
                reasoning=model.capture_reasoning,
                metadata=model.capture_metadata,
            )
        selected = None if model.selected is None else tokens[model.selected]
        return ViewModel(
            tokenizer=tokenizer_view,
            notice=None
            if tokenizer_view is not None
            else "Choose a Hugging Face tokenizer repository and revision to begin.",
            messages=[
                Message(role=role, content=content) for role, content in model.messages
            ],
            views=view_options,
            current_view=model.current_view,
            text=model.text(),
            tokens=tokens,
            selected=selected,
            capture=capture,
        )

    def load_model(self, repository: str, revision: str) -> ViewModel:
        return self._run(lambda: self._model.load(repository, revision))

    def set_messages(self, messages: list[Message]) -> ViewModel:
        pairs = [(message.role, message.content) for message in messages]
        return self._run(lambda: self._model.set_messages(pairs))

    def load_capture(self, name: str, content: str) -> ViewModel:
        def operation() -> None:
            try:
                data = json.loads(content)
            except (json.JSONDecodeError, UnicodeError) as error:
                raise TokenizerModelError(
                    f"Capture is not valid JSON: {error}"
                ) from error
            if not isinstance(data, dict):
                raise TokenizerModelError("Capture JSON must contain an object.")
            answer, reasoning = _capture_texts(data)
            metadata = {
                key: value
                for key, value in data.items()
                if key
                not in {"choices", "output", "answer", "reasoning", "reasoning_content"}
            }
            if (
                "choices" in data
                and isinstance(data["choices"], list)
                and data["choices"]
            ):
                choice = data["choices"][0]
                if isinstance(choice, dict) and "finish_reason" in choice:
                    metadata["finish_reason"] = choice["finish_reason"]
            self._model.set_capture(name, answer, reasoning, metadata)

        return self._run(operation)

    def select_view(self, key: str) -> ViewModel:
        return self._run(lambda: self._model.choose_view(key))

    def select_token(self, index: int) -> ViewModel:
        return self._run(lambda: self._model.select(index))

    def _run(self, operation: Any) -> ViewModel:
        try:
            operation()
        except TokenizerModelError as error:
            raise CommandError(str(error)) from error
        return self.view_model()


def _capture_texts(data: dict[str, Any]) -> tuple[str | None, str | None]:
    """Extract common OpenAI-compatible and Responses API text fields."""
    answer: str | None = None
    reasoning: str | None = None
    choices = data.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        message = choices[0].get("message", {})
        if isinstance(message, dict):
            answer = _as_text(message.get("content"))
            reasoning = _as_text(
                message.get("reasoning_content", message.get("reasoning"))
            )
    if answer is None:
        answer = _as_text(data.get("answer", data.get("output_text")))
    if reasoning is None:
        reasoning = _as_text(data.get("reasoning", data.get("reasoning_content")))
    output = data.get("output")
    if isinstance(output, list):
        answer_parts: list[str] = []
        reasoning_parts: list[str] = []
        for item in output:
            if not isinstance(item, dict) or not isinstance(item.get("content"), list):
                continue
            for part in item["content"]:
                if not isinstance(part, dict):
                    continue
                text = _as_text(part.get("text"))
                if text is None:
                    continue
                if part.get("type") == "reasoning_text":
                    reasoning_parts.append(text)
                else:
                    answer_parts.append(text)
        if answer is None and answer_parts:
            answer = "".join(answer_parts)
        if reasoning is None and reasoning_parts:
            reasoning = "".join(reasoning_parts)
    return answer, reasoning


def _as_text(value: object) -> str | None:
    return value if isinstance(value, str) else None
