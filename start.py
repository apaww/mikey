from rich.console import Console
from rich.markdown import Markdown
import json

template = {
    "token": "",
    "prefix": "!",
    "owner_id": 0,
    "status": "v1.0a | !help",
    "color": "0xf48f1b",
    "db_url": "mongodb://localhost:27017",
    "work": [
        90,
        100
    ],
    "beg": [
        5,
        10
    ],
    "daily": [
        100,
        1000
    ],
    "emoji": [
        "🪙"
    ],
    "worklist": [
        "Программистом",
        "Тестировщиком",
        "Верстальщиком",
        "Ютубером",
        "Стримером",
        "Модератором",
        "Веб-Художником"
    ],
    "link": "[Саппорт сервер {client.user.name}](https://google.com/)"
}

with open("config.json", 'w', encoding='utf8') as f:
    json.dump(template, f, indent=2)

console = Console()
with open("START.md", encoding='utf8') as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
