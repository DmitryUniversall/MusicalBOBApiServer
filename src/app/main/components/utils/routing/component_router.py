from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute

utils_router = APIRouter(route_class=ApplicationResponseApiRoute)
