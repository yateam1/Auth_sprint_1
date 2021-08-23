# Микросервис Auth

## Запуск приложения локально
1. Скопировать файл конфигурации
```shell
cat config/.env.template > config/.env
````
2. В файле `config/.env` заполнить секреты данными.
3. Запустить контейнеры.
```shell
docker-compose up
```
4. Перейти в браузере по адресу `0.0.0.0:8000`.
5. Провести миграции
```shell
docker-compose run --rm flask db upgrade
```
6. Прогнать тесты
```shell
docker-compose run --rm flask-api pytest
```

