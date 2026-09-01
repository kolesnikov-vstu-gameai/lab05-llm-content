"""Генераторы с валидацией: при невалидном JSON — повтор (до N раз). Считает % валидных ответов."""

import argparse
import json
import re
from pathlib import Path

from pydantic import BaseModel, ValidationError

from .llm import complete
from .schemas import DialogueTurn, Item, Quest

ROOT = Path(__file__).resolve().parents[2]
PROMPTS, OUT = ROOT / "prompts", ROOT / "data" / "out"
OUT.mkdir(parents=True, exist_ok=True)
STATS = {"calls": 0, "valid": 0}


def _extract_json(text: str) -> str:
    m = re.search(r"\{.*\}", text, re.S)
    return m.group(0) if m else text


def generate(schema: type[BaseModel], prompt_file: str, user: str, retries: int = 3) -> BaseModel:
    system = (PROMPTS / prompt_file).read_text(encoding="utf-8")
    last = None
    for _ in range(retries):
        STATS["calls"] += 1
        raw = complete(system, user)
        try:
            obj = schema.model_validate_json(_extract_json(raw))
            STATS["valid"] += 1
            return obj
        except (ValidationError, ValueError) as exc:
            last = exc
            user = f"{user}\n\nПредыдущий ответ невалиден: {exc}. Верни ТОЛЬКО JSON по схеме."
    raise RuntimeError(f"не удалось получить валидный JSON: {last}")


def gen_quest(setting: str) -> Quest:
    return generate(Quest, "quest.md", f"Сеттинг: {setting}")


def gen_item(setting: str, level: int) -> Item:
    return generate(Item, "item.md", f"Сеттинг: {setting}. Уровень игрока: {level}")


def npc_reply(npc_persona: str, history: list[dict], player_text: str) -> DialogueTurn:
    system = (PROMPTS / "npc_dialogue.md").read_text(encoding="utf-8").replace("{persona}", npc_persona)
    hist = "\n".join(f"{h['role']}: {h['text']}" for h in history[-6:])
    STATS["calls"] += 1
    raw = complete(system, f"История:\n{hist}\nИгрок: {player_text}")
    turn = DialogueTurn.model_validate_json(_extract_json(raw))
    STATS["valid"] += 1
    return turn


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quests", type=int, default=0)
    ap.add_argument("--items", type=int, default=0)
    ap.add_argument("--setting", default="тёмное фэнтези, портовый город")
    a = ap.parse_args()
    if a.quests:
        qs = [gen_quest(a.setting).model_dump() for _ in range(a.quests)]
        (OUT / "quests.json").write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.items:
        its = [gen_item(a.setting, lvl).model_dump() for lvl in range(1, a.items + 1)]
        (OUT / "items.json").write_text(json.dumps(its, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"валидных ответов: {STATS['valid']}/{STATS['calls']} = {STATS['valid'] / max(1, STATS['calls']):.0%}")
