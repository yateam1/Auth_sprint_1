from requests_oauthlib import OAuth2Session
from flask import request, redirect, session
from flask.json import jsonify
import requests

from app.settings import config
from app.services import UserService

client_id = config('GITHUB_CLIENT_ID')
client_secret = config('GITHUB_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
user_endpoint = "https://api.github.com/user"


class Github:

    def authorization(self):
        print('-----', session, session.get('oauth_state'))
        github = OAuth2Session(
            client_id,
            scope=['user:email'],
        )
        authorization_url, state = github.authorization_url(authorization_base_url)
        session['oauth_state'] = state
        self.token = state
        print('+++', state, session)
        return redirect(authorization_url)

    def callback(self):
        print('-----', session, session['oauth_state'])
        github = OAuth2Session(client_id, state=session.get('oauth_state'))
        token = github.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        # TODO добавить действия
        # По идеи надо проверить есть ли у нас пользователь с такой почтой,
        # и если есть то залогинить его. Если нет, то создать учётную запись
        # и также его залогинить. Ну и записать в таблицу social данные.

        # получаю мэйл, по нему нахожу пользователя
        user_data = requests.get(user_endpoint, headers=dict(Authorization=f"token {token}")).json()
        email = user_data.get('email')
        print('===', user_data)
        if email:
            user = UserService.get_user_by_username(user_data.get('login'))
        import json
        return json.dumps(user_data)
