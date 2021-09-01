from app.services.permissions import RoleService
from app.services.sessions import HistoryService, SessionService
from app.services.users import ProfileService, UserService
from app.services.auth import JWTService, AuthService


services = {f'{k[:-7].lower()}_service': v for k, v in globals().items() if k.endswith('Service')}

for k, v in services.items():
    globals()[k] = v()

__all__ = list(services.keys())
