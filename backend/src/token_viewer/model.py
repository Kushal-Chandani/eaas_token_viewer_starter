"""A Hugging Face tokenizer model that computes the token viewer's domain state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class TokenizerModelError(Exception):
    """An operation could not be completed without changing current state."""


@dataclass(frozen=True)
class TokenData:
    """One token and its offsets in a rendered string."""

    token_id: int
    piece: str
    text: str
    start: int
    end: int
    special: bool


@dataclass(frozen=True)
class TokenViewData:
    """Text and tokens for one selectable representation."""

    title: str
    text: str
    tokens: list[TokenData]


class TokenizerModel:
    """Own the loaded tokenizer, current chat, capture, view and selection."""

    def __init__(self) -> None:
        self.repository: str | None = None
        self.revision: str | None = None
        self.tokenizer: Any = None
        self.messages: list[tuple[str, str]] = [("user", "Show me some tokens.")]
        self.views: dict[str, TokenViewData] = {}
        self.current_view: str | None = None
        self.selected: int | None = None
        self.capture_name: str | None = None
        self.capture_answer: str | None = None
        self.capture_reasoning: str | None = None
        self.capture_metadata: dict[str, object] = {}

    def load(self, repository: str, revision: str) -> None:
        """Load a fast tokenizer and prepare views before committing the change."""
        if not repository.strip() or not revision.strip():
            raise TokenizerModelError("Give both a repository and a revision.")
        try:
            from transformers import AutoTokenizer

            tokenizer = AutoTokenizer.from_pretrained(
                repository.strip(), revision=revision.strip(), use_fast=True
            )
            if not tokenizer.is_fast:
                raise TokenizerModelError(
                    "This repository has no fast tokenizer; offset display needs one."
                )
            views = self._build_views(tokenizer, self.messages)
        except TokenizerModelError:
            raise
        except Exception as error:
            raise TokenizerModelError(
                f"Could not load tokenizer {repository!r} at revision {revision!r}: {error}"
            ) from error
        self.tokenizer = tokenizer
        self.repository = repository.strip()
        self.revision = revision.strip()
        self.views = views
        self.current_view = "chat"
        self.selected = None

    def set_messages(self, messages: list[tuple[str, str]]) -> None:
        """Compute new token views first, then replace the current chat."""
        if not messages:
            raise TokenizerModelError("Give at least one message.")
        if self.tokenizer is None:
            raise TokenizerModelError("Load a tokenizer before setting messages.")
        views = self._build_views(self.tokenizer, messages)
        self.messages = messages.copy()
        self.views = views
        self.selected = None

    def choose_view(self, key: str) -> None:
        if key not in self.views:
            raise TokenizerModelError(f"There is no view {key!r}.")
        self.current_view = key
        self.selected = None

    def select(self, index: int) -> None:
        count = len(self.tokens())
        if not 0 <= index < count:
            raise TokenizerModelError(
                f"There is no token {index}: this view has {count}, numbered from 0."
            )
        self.selected = index

    def set_capture(
        self,
        name: str,
        answer: str | None,
        reasoning: str | None,
        metadata: dict[str, object],
    ) -> None:
        self.capture_name = name
        self.capture_answer = answer
        self.capture_reasoning = reasoning
        self.capture_metadata = metadata

    def text(self) -> str:
        return "" if self.current_view is None else self.views[self.current_view].text

    def tokens(self) -> list[TokenData]:
        return [] if self.current_view is None else self.views[self.current_view].tokens

    def _build_views(
        self, tokenizer: Any, messages: list[tuple[str, str]]
    ) -> dict[str, TokenViewData]:
        message_dicts = [
            {"role": role, "content": content} for role, content in messages
        ]
        try:
            chat_text = tokenizer.apply_chat_template(
                message_dicts,
                tokenize=False,
                add_generation_prompt=False,
                enable_thinking=False,
            )
        except Exception as error:
            raise TokenizerModelError(
                f"Could not apply this tokenizer's chat template: {error}"
            ) from error
        plain_text = "\n".join(content for _, content in messages)
        return {
            "chat": TokenViewData(
                "Chat, after the model's chat template",
                chat_text,
                self._encode(tokenizer, chat_text),
            ),
            "text": TokenViewData(
                "Message text alone", plain_text, self._encode(tokenizer, plain_text)
            ),
        }

    @staticmethod
    def _encode(tokenizer: Any, text: str) -> list[TokenData]:
        try:
            encoded = tokenizer(
                text, add_special_tokens=False, return_offsets_mapping=True
            )
            ids = encoded["input_ids"]
            offsets = encoded["offset_mapping"]
            special_ids = set(tokenizer.all_special_ids)
            result: list[TokenData] = []
            for token_id, pair in zip(ids, offsets, strict=True):
                start, end = int(pair[0]), int(pair[1])
                result.append(
                    TokenData(
                        token_id=int(token_id),
                        piece=str(tokenizer.convert_ids_to_tokens(int(token_id))),
                        text=text[start:end],
                        start=start,
                        end=end,
                        special=int(token_id) in special_ids,
                    )
                )
            return result
        except Exception as error:
            raise TokenizerModelError(
                f"Could not tokenize rendered text: {error}"
            ) from error
