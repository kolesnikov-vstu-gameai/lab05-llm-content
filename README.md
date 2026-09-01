# Лабораторная работа № 5. Генерация игрового контента с помощью LLM

Дисциплина «Игровой искусственный интеллект» · Максимум **20 баллов** (+5 за задание со звёздочкой)

**Студент:** ФИО, группа · **Вариант стека:** … · **Видео:** <ссылка> · **Отчёт:** `docs/report.md` → PDF

## Стек

Python · OpenAI / Anthropic / Ollama · pydantic · Streamlit

## Что нужно сдать

- [ ] 3 генератора (квесты, предметы, диалоги) с валидацией
- [ ] Корпус: 10 квестов + 20 предметов
- [ ] Диалоговая система с 3+ NPC
- [ ] Streamlit-демо или ноутбук
- [ ] Отчёт PDF 6–8 стр.: промпты, примеры, % валидных JSON, разнообразие

Полное задание, критерии оценки и типичные ошибки — в методических указаниях (ЛР № 5).

## Структура

```
src/lab05/llm.py           единый клиент: OpenAI / Anthropic / Ollama (переключение через .env)
src/lab05/schemas.py       pydantic-схемы Quest, Item, DialogueTurn
src/lab05/generators.py    3 генератора с валидацией и повтором при невалидном JSON
prompts/*.md               системные промпты (версионируются!)
data/out/                  корпус: quests.json, items.json
app/streamlit_app.py       демо
```

```bash
cp .env.example .env   # вписать ключ или LLM_PROVIDER=ollama
pip install -e ".[dev]"
python -m lab05.generators --quests 10 --items 20
streamlit run app/streamlit_app.py
```

## Как сдавать

1. Работайте в этом репозитории, коммитьте по шагам (`step-1`, `step-2` …) — история коммитов учитывается.
2. Отчёт пишите в `docs/report.md`, экспортируйте в PDF в `docs/report.pdf` (Times New Roman 12, 1,5, 6–8 стр.).
3. Видео — на YouTube/Диск, ссылку в README и в отчёт. Файлы видео в git не кладём.
4. Готовую работу отметьте тегом `git tag v1.0 && git push --tags` и создайте Release.
