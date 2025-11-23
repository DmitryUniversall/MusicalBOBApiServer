from http import HTTPStatus

from src.base.utils.types import UUIDString
from ..domain.entities import AuthSessionInternal
from ..domain.exceptions import InvalidSessionHTTPException, InactiveSessionHTTPException
from ..domain.repositories import AuthSessionRepositoryI
from ..domain.services import AuthSessionServiceI


class AuthSessionServiceImpl(AuthSessionServiceI):
    def __init__(self, auth_session_repository: AuthSessionRepositoryI) -> None:
        self._auth_session_repository: AuthSessionRepositoryI = auth_session_repository

    def generate_session_uuid(self) -> str:
        return self._auth_session_repository.generate_session_uuid()

    async def _validate_session(self, session: AuthSessionInternal) -> None:
        if not session.is_active:
            raise InactiveSessionHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    async def get_session(self, user_id: int, session_uuid: UUIDString) -> AuthSessionInternal:
        if (session := await self._auth_session_repository.get_session(user_id, session_uuid)) is not None:
            return session

        raise InvalidSessionHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    async def revoke_session(self, user_id: int, session_uuid: UUIDString) -> None:
        success = await self._auth_session_repository.revoke_session_by_id(user_id, session_uuid)
        if not success:
            raise InvalidSessionHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    async def create_session(
            self,
            user_id: int,
            ip_address: str,
            user_agent: str,
            session_name: str,
            access_token_uuid: UUIDString,
            refresh_token_uuid: UUIDString
    ) -> AuthSessionInternal:
        return await self._auth_session_repository.create_session(
            user_id, ip_address, user_agent, session_name, access_token_uuid, refresh_token_uuid
        )

    async def get_user_sessions(self, user_id: int) -> tuple[AuthSessionInternal, ...]:
        return await self._auth_session_repository.get_user_sessions(user_id)

    async def update_session(self, updated_session: AuthSessionInternal) -> None:
        await self._auth_session_repository.update_session(updated_session)

    async def revoke_other_sessions(self, user_id: int, keep_session_uuid: UUIDString) -> None:
        return await self._auth_session_repository.revoke_other_sessions(user_id, keep_session_uuid)

    async def get_session_from_access_token(self, access_token: str) -> AuthSessionInternal:
        session = await self._auth_session_repository.get_session_from_access_token(access_token)
        await self._validate_session(session)  # TODO: Make it better (1 gateway for getting sessions to perform validation in 1 place)
        return session

    async def get_session_from_refresh_token(self, refresh_token: str) -> AuthSessionInternal:
        session = await self._auth_session_repository.get_session_from_refresh_token(refresh_token)

        await self._validate_session(session)  # TODO: Make it better (1 gateway for getting sessions to perform validation in 1 place)
        return session
