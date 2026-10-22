"""Parse an agent reply into (price, notes)."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

_JSON_OBJECT = re.compile(r"\{.*?\}", re.DOTALL)
_PRICE_FIELD = re.compile(r'"?price"?\s*[:=]\s*\$?\s*(-?\d+(?:\.\d+)?)', re.IGNORECASE)
_NOTES_FIELD = re.compile(r'"notes"\s*:\s*"(.*?)"', re.DOTALL)


@dataclass
class ParsedReply:
    price: float | None
    notes: str
    ok: bool


def parse_reply(text: str, price_min: float, price_max: float) -> ParsedReply:
    """Return the price and notes from a reply.

    The parser tries each JSON object in the text, then a regex on "price".
    A price outside [price_min, price_max] or a non-finite price is a failure.
    """
    price: float | None = None
    notes = ""

    for match in _JSON_OBJECT.finditer(text):
        try:
            obj = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "price" in obj:
            try:
                price = float(obj["price"])
            except (TypeError, ValueError):
                price = None
            notes = str(obj.get("notes", ""))
            break

    if price is None:
        m = _PRICE_FIELD.search(text)
        if m:
            price = float(m.group(1))
        n = _NOTES_FIELD.search(text)
        if n:
            notes = n.group(1)

    if price is None or not math.isfinite(price) or not (price_min <= price <= price_max):
        return ParsedReply(price=None, notes=notes, ok=False)
    return ParsedReply(price=round(price, 4), notes=notes[:600], ok=True)
