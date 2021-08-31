from requests_oauthlib import OAuth2Session
from flask import request, redirect, session
from flask.json import jsonify
import requests
import json
from urllib.parse import parse_qs

from app.settings import config
from app.services.users import UserService
from app.services.social import SocialService

client_id = config('GITHUB_CLIENT_ID')
client_secret = config('GITHUB_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
user_endpoint = "https://api.github.com/user"


class Github:

    def authorization(self):
        github = OAuth2Session(
            client_id,
            scope=['user:email'],
        )
        authorization_url, state = github.authorization_url(authorization_base_url)
        session['oauth_state'] = state
        return redirect(authorization_url)

    def callback(self, state=None):
        github = OAuth2Session(client_id, state=request.args.get('state'))
        try:
            res = requests.post(
                token_url,
                data=dict(
                    client_id=client_id,
                    client_secret=client_secret,
                    code=request.args.get('code'),
                ),
            )
            res = parse_qs(res.content.decode("utf-8"))
            token = res["access_token"][0]
        except Exception as e:
            return str(e)
        # TODO добавить действия
        # По идеи надо проверить есть ли у нас пользователь с такой почтой,
        # и если есть то залогинить его. Если нет, то создать учётную запись
        # и также его залогинить. Ну и записать в таблицу social данные.

        user_data = requests.get(user_endpoint, headers=dict(Authorization=f"token {token}")).json()
        email = user_data.get('email')
        if email:
            user = UserService.get_user_by_username(user_data.get('login'))
            if user:
                SocialService.create(provider='github', token=token, user=user)
        return json.dumps(user_data)
