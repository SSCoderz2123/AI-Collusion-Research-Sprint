"""Parse an agent reply into (price, notes)."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

_DECODER = json.JSONDecoder()
# Fallbacks for replies without valid JSON. A quoted key is the strongest signal.
_QUOTED_PRICE = re.compile(r'"price"\s*:\s*"?\$?\s*(-?\d+(?:\.\d+)?)', re.IGNORECASE)
_BARE_PRICE = re.compile(r"\bprice\s*[:=]\s*\$?\s*(-?\d+(?:\.\d+)?)", re.IGNORECASE)
_NOTES_FIELD = re.compile(r'"notes"\s*:\s*"(.*?)"', re.DOTALL)


@dataclass
class ParsedReply:
    price: float | None
    notes: str
    ok: bool


def _find_price_object(obj) -> dict | None:
    """Return the first dict (depth-first) that has a "price" key."""
    if isinstance(obj, dict):
        if "price" in obj:
            return obj
        children = obj.values()
    elif isinstance(obj, list):
        children = obj
    else:
        return None
    for child in children:
        found = _find_price_object(child)
        if found is not None:
            return found
    return None


def _json_objects(text: str):
    """Yield every JSON value that starts at a "{" in the text.

    raw_decode handles braces inside strings and nested objects, which a regex cannot.
    """
    pos = text.find("{")
    while pos != -1:
        try:
            obj, end = _DECODER.raw_decode(text, pos)
        except json.JSONDecodeError:
            pos = text.find("{", pos + 1)
            continue
        yield obj
        pos = text.find("{", end)


def parse_reply(text: str, price_min: float, price_max: float) -> ParsedReply:
    """Return the price and notes from a reply.

    Order: JSON object with a "price" key; then a quoted "price" key; then the last
    bare "price: x" in the text (the final answer usually comes last). A price outside
    [price_min, price_max] or a non-finite price is a failure.
    """
    price: float | None = None
    notes = ""

    for obj in _json_objects(text):
        hit = _find_price_object(obj)
        if hit is None:
            continue
        try:
            price = float(hit["price"])
        except (TypeError, ValueError):
            price = None
        notes = str(hit.get("notes", ""))
        break

    if price is None:
        quoted = _QUOTED_PRICE.findall(text)
        bare = _BARE_PRICE.findall(text)
        if quoted:
            price = float(quoted[0])
        elif bare:
            price = float(bare[-1])
        n = _NOTES_FIELD.search(text)
        if n:
            notes = n.group(1)

    if price is None or not math.isfinite(price) or not (price_min <= price <= price_max):
        return ParsedReply(price=None, notes=notes, ok=False)
    return ParsedReply(price=round(price, 4), notes=notes[:600], ok=True)
