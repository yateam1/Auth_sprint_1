# Микросервис Auth
## Демо
https://yandex.in.net
## Запуск приложения в проде
1. Скопировать файл конфигурации
```shell
cat config/.env.template > config/.env
````
2. В файле `config/.env` заполнить секреты данными.
3. Запустить контейнеры.
```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```
## Запуск приложения локально
1. Скопировать файл конфигурации
```shell
cat config/.env.template > config/.env
````
2. В файле `config/.env` заполнить секреты данными.
3. Провести миграции.
```shell
docker-compose run --rm flask db upgrade
```
4. Запустить контейнеры.
```shell
docker-compose up
```
5. Перейти в браузере по адресу `0.0.0.0:8000`.
## Запуск тестов
```shell
docker-compose run --rm flask-api pytest
```

