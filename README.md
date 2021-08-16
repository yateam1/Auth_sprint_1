# Микросервис авторизации/аутентификации

## Архитектура
В качестве веб-сервера используется caddy, как наиболее простой в настройке, но в тоже время и функциональный.
Основное хранилище данных — Postgres, для хранения сессий используется Redis.

![diagram](https://316129.selcdn.ru/public/diagram.png)

## Модели данных
Пользователь:
- e-mail(login)
- password
- имя пользователя
- is_superuser
- role (связь с таблицей ролей)

Роль:
- название. Например контент-менеджер, подписчик, гость.

История аутентификаций:
- user_id (связь с таблицей пользователей),
- [useragent](https://ru.wikipedia.org/wiki/User_agent#:~:text=User%20agent%20—%20идентификационная%20строка,со%20встроенным%20доступа%20к%20веб-ресурсам),
- дата регистрации,
- дата последней аутентификации


## OpenApi документация
### регистрация пользователя:
  POST api/v1/user/
 вход пользователя в аккаунт:
  api/v1/user/login
 обновление access-токена:
  GET: api/v1/token/refresh
 выход пользователя из аккаунта:
  api/v1/user/logout
 изменение логина или пароля:
  PUT api/v1/user/{id}
 получение пользователем своей истории входов в аккаунт:
  GET api/v1/user/history


### api для управления доступами

 crud для управления ролями:

 POST api/v1/roles
 DELETE api/v1/roles
 PUT api/v1/roles
 GET api/v1/roles

 назначить пользователю роль:
 POST api/v1/user/{id}/role/{role_id}
 отобрать у пользователя роль:
 DELETE api/v1/user/{id}/role/{role_id}
 метод для проверки наличия прав у пользователя:
 GET api/v1/user/{id}/role


