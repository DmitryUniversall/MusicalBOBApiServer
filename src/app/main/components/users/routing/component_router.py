from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute

users_router = APIRouter(route_class=ApplicationResponseApiRoute)
