# Микросервис авторизации/аутентификации

## Архитектура
В качестве веб-сервера используется caddy, как наиболее простой в настройке, но в тоже время и функциональный.
Основное хранилище данных — Postgres, для хранения сессий используется Redis.

![diagram](https://316129.selcdn.ru/public/diagram.png)

## Модели данных
![image](https://user-images.githubusercontent.com/58282452/129549569-56ccbc52-bcb5-48f1-b699-baebc7b75f6b.png)

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


