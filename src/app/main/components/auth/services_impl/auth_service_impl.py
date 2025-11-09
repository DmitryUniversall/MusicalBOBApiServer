from http import HTTPStatus

from src.app.main.components.users import UserInternal, UsersServiceI
from src.base.exceptions import DoesNotExistError
from src.base.utils.types import UUIDString
from ..domain import (
    AuthInfo,
    AuthSessionInternal,
    AuthTokenPair,
    AuthRepositoryI,
    AuthServiceI,
    AuthSessionServiceI,
    SuspiciousActivityHTTPException,
    WrongAuthCredentialsHTTPException,
    AuthUserUnknownHTTPException,
)


class AuthServiceImpl(AuthServiceI):
    def __init__(
            self,
            auth_repository: AuthRepositoryI,
            session_service: AuthSessionServiceI,
            user_service: UsersServiceI
    ) -> None:
        self._auth_repository = auth_repository
        self._session_service: AuthSessionServiceI = session_service
        self._user_service: UsersServiceI = user_service

    async def _log_security_event(self) -> None:  # TODO
        pass

    async def _get_user_by_id(self, user_id: int) -> UserInternal:
        try:
            return await self._user_service.get_user_by_id(user_id)
        except DoesNotExistError as error:
            raise AuthUserUnknownHTTPException() from error

    async def _revoke_session(self, user_id: int, session_uuid: UUIDString) -> None:
        await self._session_service.revoke_session(user_id, session_uuid)

    async def _handle_suspicious_activity(self, user: UserInternal, session: AuthSessionInternal) -> None:
        await self._log_security_event()
        await self._revoke_session(user.id, session.session_uuid)

    async def suspicious_activity_check(self, session: AuthSessionInternal, current_client_ip: str, current_client_user_agent: str) -> bool:
        return session.ip_address == current_client_ip and session.user_agent == current_client_user_agent

    async def _register_user(self, username: str, password: str, **field) -> UserInternal:
        return await self._user_service.create_user(username, password, **field)

    async def _login_user(self, username: str, password: str, **fields) -> UserInternal:
        try:
            return await self._user_service.get_by_auth_credentials(username=username, password_raw=password, **fields)
        except DoesNotExistError as error:
            raise WrongAuthCredentialsHTTPException() from error

    async def _create_session(
            self,
            user: UserInternal,
            ip_address: str,
            user_agent: str,
            session_name: str
    ) -> tuple[AuthInfo, AuthTokenPair]:
        access_token_uuid = self._auth_repository.generate_jwt_token_id()
        refresh_token_uuid = self._auth_repository.generate_jwt_token_id()

        session = await self._session_service.create_session(
            user.id, ip_address, user_agent, session_name, access_token_uuid, refresh_token_uuid
        )

        access_token = self._auth_repository.create_access_token(user.id, session.session_uuid, token_uuid=access_token_uuid)
        refresh_token = self._auth_repository.create_refresh_token(user.id, session.session_uuid, token_uuid=refresh_token_uuid)

        token_pair = AuthTokenPair(
            access_token=access_token,
            refresh_token=refresh_token
        )

        auth_info = AuthInfo(
            user=user,
            session=session
        )

        return auth_info, token_pair

    async def authenticate(self, access_token: str) -> AuthInfo:
        session = await self._session_service.get_session_from_access_token(access_token)
        user = await self._get_user_by_id(session.user_id)
        return AuthInfo(user=user, session=session)

    async def refresh(self, refresh_token: str, current_client_ip: str, current_client_user_agent: str) -> AuthTokenPair:
        session = await self._session_service.get_session_from_refresh_token(refresh_token)
        user = await self._get_user_by_id(session.user_id)

        if not await self.suspicious_activity_check(session, current_client_ip, current_client_user_agent):
            await self._handle_suspicious_activity(user, session)
            raise SuspiciousActivityHTTPException(status_code=HTTPStatus.FORBIDDEN)

        new_access_token_uuid = self._auth_repository.generate_jwt_token_id()
        new_refresh_token_uuid = self._auth_repository.generate_jwt_token_id()

        new_access_token = self._auth_repository.create_access_token(user.id, session.session_uuid, token_uuid=new_access_token_uuid)
        new_refresh_token = self._auth_repository.create_refresh_token(user.id, session.session_uuid, token_uuid=new_refresh_token_uuid)

        session.access_token_uuid = new_access_token_uuid
        session.refresh_token_uuid = new_refresh_token_uuid

        await self._session_service.update_session(session)

        return AuthTokenPair(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    async def register(
            self,
            username: str,
            password: str,
            ip_address: str,
            user_agent: str,
            session_name: str,
            **user_fields
    ) -> tuple[AuthInfo, AuthTokenPair]:
        user = await self._register_user(username, password, **user_fields)
        return await self._create_session(user, ip_address, user_agent, session_name)

    async def login(
            self,
            username: str,
            password: str,
            ip_address: str,
            user_agent: str,
            session_name: str,
            **user_fields
    ) -> tuple[AuthInfo, AuthTokenPair]:
        user = await self._login_user(username, password, **user_fields)
        return await self._create_session(user, ip_address, user_agent, session_name)

    async def revoke_session(self, user_id: int, session_uuid: UUIDString) -> None:
        await self._session_service.revoke_session(user_id, session_uuid)
