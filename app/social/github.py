from urllib.parse import parse_qs
import json

from requests_oauthlib import OAuth2Session
from flask import request, redirect, session
import requests

from app.settings import config
from app.services import user_service, profile_service
from app.services.auth import AuthService
from app.services.users import UserService
from app.services.users import ProfileService

client_id = config('GITHUB_CLIENT_ID')
client_secret = config('GITHUB_CLIENT_SECRET')
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
user_endpoint = "https://api.github.com/user"

profile_service = ProfileService()
user_service = UserService()
auth_service = AuthService()

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
        github_id = user_data.get('id')

        profile = profile_service.get_by_email(email=email)
        profile = profile.user if profile else user_service.get_user_by_username(username=login)
        if profile:
            user_service.update(profile, github_id=github_id)
        else:
            profile = user_service.create(
                username=login,
                email=email,
                github_id=github_id,
                password=UserService.generate_password(),
            )
        auth_service.auth(True, profile)

        return json.dumps(user_data)
