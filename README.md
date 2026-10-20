# github-osint

Утилита собирает открытую информацию о пользователе GitHub и присылает сводку в Telegram. В сводку попадают данные профиля, список публичных репозиториев и адреса почты из коммитов.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

Впиши свои токены в `config.py` и передай логин.

```bash
python main.py octocat
```

## Тесты

```bash
pytest
```
