# Wallet REST API

## Запуск

``` bash
cp .env.example .env && docker compose up --build
```

### Тесты

``` bash
docker compose --profile test up -d
uv sync
uv run pytest tests/ -v
```

