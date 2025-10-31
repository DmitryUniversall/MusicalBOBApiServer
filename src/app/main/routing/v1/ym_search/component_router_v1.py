from fastapi import APIRouter

from src.app.main.common.http import ApplicationResponseApiRoute

ym_search_router_v1 = APIRouter(route_class=ApplicationResponseApiRoute)
