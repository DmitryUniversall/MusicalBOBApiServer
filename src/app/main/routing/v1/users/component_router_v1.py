from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute

users_router_v1 = APIRouter(route_class=ApplicationResponseApiRoute)
