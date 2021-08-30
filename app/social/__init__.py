from flask import Blueprint

from app.social.github import Github
from app.social.mailru import MailRu


social_blueprint = Blueprint('social', __name__, url_prefix='/social')


providers = {
    'github': Github,
    'mailru': MailRu,
}


def f(function_name: str, provider: str):
    provider_class = providers.get(provider.lower())
    if not provider_class:
        return 'Неизвестный провайдер.'
    return getattr(provider_class(), function_name)()


@social_blueprint.route('/<provider>/')
def authorization(provider):
    return f('authorization', provider)


@social_blueprint.route('/<provider>/callback/')
def callback(provider):
    return f('callback', provider)
