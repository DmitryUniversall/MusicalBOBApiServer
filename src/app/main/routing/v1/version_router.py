from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute
from .auth import auth_router_v1
from .users import users_router_v1
from .utils import utils_router_v1
from .ym_search import ym_search_router_v1

# Make sure that all endpoints implement base server interface
assert auth_router_v1.route_class is ApplicationResponseApiRoute
assert utils_router_v1.route_class is ApplicationResponseApiRoute
assert users_router_v1.route_class is ApplicationResponseApiRoute

v1_router = APIRouter(route_class=ApplicationResponseApiRoute)
v1_router.include_router(auth_router_v1, prefix="/auth")
v1_router.include_router(users_router_v1, prefix="/users")
v1_router.include_router(utils_router_v1, prefix="/utils")
v1_router.include_router(ym_search_router_v1, prefix="/search/ym")
