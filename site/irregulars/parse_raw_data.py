#!/usr/bin/env python3
"""Parse wiki-table raw_data.txt into JSON."""

import json
import re
from pathlib import Path


def extract_item_name(cell: str) -> tuple[str, int, dict]:
    """Return (name, quantity, style_flags). Style: bold, italic from wiki markup."""
    s = cell.strip()
    style = {"bold": False, "italic": False}
    if s.startswith("'''"):
        style["bold"] = True
    elif s.startswith("''") and not s.startswith("'''"):
        style["italic"] = True
    qty = 1
    m_qty = re.search(r"\bx(\d+)\s*$", s)
    if m_qty:
        qty = int(m_qty.group(1))
    # First arg of item icon is the display name (before optional |qty= etc.)
    m = re.search(r"\{\{item icon\|([^}]+)\}\}", cell)
    if m:
        inner = m.group(1)
        name = inner.split("|", 1)[0].strip()
        return name, qty, style
    return cell.strip(), qty, style


def strip_refs_for_plain(source: str) -> str:
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", source, flags=re.DOTALL)
    s = re.sub(r"<ref[^/]*/>", "", s)
    return s.strip()


def parse_tomestone(cost_cell: str) -> int | None:
    m = re.search(r"\{\{tomestone\|irraphorism\|(\d+)\}\}", cost_cell)
    return int(m.group(1)) if m else None


def iter_table_rows(lines: list[str]):
    """Wiki tables often put '|-' on its own line; cells follow on the next line."""
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.strip() == "|-":
            i += 1
            if i >= len(lines):
                break
            line = lines[i].rstrip()
            if "||" not in line:
                i += 1
                continue
            rest = line.lstrip()
            if rest.startswith("|"):
                rest = rest[1:].lstrip()
            yield rest
            i += 1
            continue
        if line.startswith("|-") and "||" in line:
            rest = line[2:].lstrip()
            if rest.startswith("|"):
                rest = rest[1:].lstrip()
            yield rest
            i += 1
            continue
        i += 1


def main() -> None:
    raw_path = Path(__file__).parent / "raw_data.txt"
    lines = raw_path.read_text(encoding="utf-8").splitlines()
    rewards = []
    for rest in iter_table_rows(lines):
        if "! Item" in rest or "! Cost" in rest:
            continue
        if rest.startswith("!"):
            continue
        parts = re.split(r"\s*\|\|\s*", rest)
        if len(parts) < 3:
            continue
        item_cell, cost_cell, source_cell = parts[0], parts[1], parts[2]
        cost = parse_tomestone(cost_cell)
        if cost is None:
            continue
        name, qty, style = extract_item_name(item_cell)
        entry = {
            "item": name,
            "quantity": qty,
            "cost_irraphorism": cost,
            "original_source": source_cell.strip(),
            "original_source_plain": strip_refs_for_plain(source_cell),
            "style": style,
            "item_cell_raw": item_cell.strip(),
        }
        rewards.append(entry)

    out_path = Path(__file__).parent / "raw_data.json"
    out_path.write_text(
        json.dumps({"title": "Rewards", "rewards": rewards}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(rewards)} rows to {out_path}")


if __name__ == "__main__":
    main()
