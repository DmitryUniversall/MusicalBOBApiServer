from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute

from src.app.main.components.auth.routing import auth_router
from src.app.main.components.users.routing import users_router
from src.app.main.components.utils.routing import utils_router

# Make sure that all endpoints implement base server interface
assert auth_router.route_class is ApplicationResponseApiRoute
assert utils_router.route_class is ApplicationResponseApiRoute
assert users_router.route_class is ApplicationResponseApiRoute

v1_router = APIRouter(route_class=ApplicationResponseApiRoute)
v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(utils_router, prefix="/utils")
v1_router.include_router(users_router, prefix="/users")
