from requests_oauthlib import OAuth2Session
from flask import request, redirect, session
from flask.json import jsonify

from app.settings import config

client_id = config('MAILRU_CLIENT_ID')
client_secret = config('MAILRU_CLIENT_SECRET')
authorization_base_url = 'https://oauth.mail.ru/login'
token_url = 'https://oauth.mail.ru/token'


class MailRu:
    def authorization(self):
        mailru = OAuth2Session(
            client_id,
            scope=['user:email'],
        )
        authorization_url, state = mailru.authorization_url(authorization_base_url)
        session['oauth_state'] = state
        return redirect(authorization_url)

    def callback(self):
        mailru = OAuth2Session(client_id, state=session['oauth_state'])
        token = mailru.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        # TODO добавить действия
        # По идеи надо проверить есть ли у нас пользователь с такой почтой,
        # и если есть то залогинить его. Если нет, то создать учётную запись
        # и также его залогинить. Ну и записать в таблицу social данные.
