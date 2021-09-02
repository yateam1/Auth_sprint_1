from requests_oauthlib import OAuth2Session
from flask import request, redirect, session
from flask.json import jsonify
import requests
import json
from urllib.parse import parse_qs
from random import randint

from app.settings import config
from app.services.users import UserService
from app.services.users import ProfileService
from app.services.social import SocialService

client_id = config('GITHUB_CLIENT_ID')
client_secret = config('GITHUB_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
user_endpoint = "https://api.github.com/user"

profile_service = ProfileService()
user_service = UserService()
social_service = SocialService()

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
        login = user_data.get('login')
        user = None
        if email:
            profile = profile_service.get_by_email(email=email)
            if profile:
                user = profile.user
        if not user:
            if login:
                user = user_service.get_user_by_username(username=login)
        if not user:
            rand_num = ''.join(["{}".format(randint(0, 9)) for num in range(0, 10)])
            passw = UserService.generate_password()
            login = login or f'temp_login_{rand_num}'
            email = email or f'temp_login_{rand_num}'
            user = user_service.create(
                username=login,
                email=email,
                password=passw,
            )
        social_service.create(provider='github', token={'token': token}, user=user)
        user_data['auth_password'] = passw
        user_data['auth_login'] = login
        user_data['auth_email'] = email
        return json.dumps(user_data)
