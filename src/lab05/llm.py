"""Единый интерфейс к LLM. Возвращает текст; JSON парсит вызывающая сторона."""

import os

from dotenv import load_dotenv

load_dotenv()
PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def complete(system: str, user: str, temperature: float = 0.8, max_tokens: int = 800) -> str:
    if PROVIDER == "openai":
        from openai import OpenAI

        r = OpenAI().chat.completions.create(model=MODEL, temperature=temperature, max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content
    if PROVIDER == "anthropic":
        import anthropic

        r = anthropic.Anthropic().messages.create(
            model=MODEL, max_tokens=max_tokens, temperature=temperature,
            system=system, messages=[{"role": "user", "content": user}])
        return r.content[0].text
    if PROVIDER == "ollama":
        import requests

        r = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": os.getenv("OLLAMA_MODEL", "llama3"), "stream": False,
                  "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            timeout=120)
        return r.json()["message"]["content"]
    raise ValueError(f"unknown provider {PROVIDER}")
