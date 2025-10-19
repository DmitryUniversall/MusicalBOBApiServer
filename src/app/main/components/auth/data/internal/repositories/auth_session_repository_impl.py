from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from src.app.main.common.redis import RedisClientMixin
from src.app.main.common.utils.redis import convert_for_redis
from src.app.main.components.auth.domain import AuthSessionRepository, AuthSessionInternal
from src.app.main.components.auth.domain.exceptions import InvalidSessionHTTPException, TokenExpiredHTTPException
from src.app.main.components.auth.internal_utils import decode_refresh_token_with_http_exceptions, decode_access_token_with_http_exceptions
from src.base.state import project_settings
from src.base.utils.types import UUIDString


class AuthSessionRepositoryRedisImpl(RedisClientMixin, AuthSessionRepository):
    AUTH_USER_DATA_REDIS_KEY: str = project_settings.AUTH_REDIS_KEY + ":user:{}"
    AUTH_USER_SESSIONS_REDIS_KEY: str = AUTH_USER_DATA_REDIS_KEY + ":sessions"
    AUTH_USER_SESSION_REDIS_KEY: str = AUTH_USER_SESSIONS_REDIS_KEY + ":{}"

    def __init__(self) -> None:
        super().__init__(db=project_settings.AUTH_REDIS_DB_ID)

    def _get_session_key(self, user_id: int, session_uuid: UUIDString) -> str:
        return self.AUTH_USER_SESSION_REDIS_KEY.format(user_id, session_uuid)

    def _get_user_sessions_key(self, user_id: int) -> UUIDString:
        return self.AUTH_USER_SESSIONS_REDIS_KEY.format(user_id)

    async def __save_session(self, session: AuthSessionInternal) -> None:
        redis = await self.get_redis()

        session_key = self._get_session_key(session.user_id, session.session_uuid)
        await redis.hset(session_key, mapping=convert_for_redis(session.to_json_dict()))  # type: ignore
        await redis.expire(session_key, round(session.expires_at.timestamp()))  # type: ignore

    async def __delete_session(self, user_id: int, session_uuid: UUIDString, *, soft: bool) -> bool:
        redis = await self.get_redis()
        session_key = self._get_session_key(user_id, session_uuid)

        if not await redis.exists(session_key):
            return False

        if soft:
            # Soft delete: update the "is_active" field to False
            await redis.hset(session_key, "is_active", "false")  # type: ignore
        else:
            await redis.delete(session_key)

        return True

    async def __get_session(self, user_id: int, session_uuid: UUIDString) -> AuthSessionInternal | None:
        redis = await self.get_redis()
        session_key = self._get_session_key(user_id, session_uuid)

        if (session_data := await redis.hgetall(session_key)) is None or len(session_data) == 0:  # type: ignore
            return None

        return AuthSessionInternal.model_validate(session_data)

    async def __scan_for_user_sessions(self, user_id: int) -> tuple[AuthSessionInternal, ...]:
        redis = await self.get_redis()

        session_uuids = tuple(key async for key in redis.scan_iter(match=self._get_user_sessions_key(user_id)))  # type: ignore
        sessions = await asyncio.gather(*(redis.hgetall(key) for key in session_uuids))  # type: ignore

        return tuple(map(AuthSessionInternal.model_validate, sessions))

    def generate_session_uuid(self) -> str:
        return str(uuid4())

    async def create_session(
            self,
            user_id: int,
            ip_address: str,
            user_agent: str,
            session_name: str,
            access_token_uuid: UUIDString,
            refresh_token_uuid: UUIDString
    ) -> AuthSessionInternal:
        session_uuid = self.generate_session_uuid()

        session = AuthSessionInternal(
            session_uuid=session_uuid,
            user_id=user_id,
            access_token_uuid=access_token_uuid,
            refresh_token_uuid=refresh_token_uuid,
            session_name=session_name,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(),
            last_used=datetime.now(),
            expires_at=datetime.now()
        )

        await self.__save_session(session)
        return session

    async def get_session(self, user_id: int, session_uuid: UUIDString) -> AuthSessionInternal | None:
        return await self.__get_session(user_id, session_uuid)

    async def get_user_sessions(self, user_id: int) -> tuple[AuthSessionInternal, ...]:
        return await self.__scan_for_user_sessions(user_id)

    async def revoke_session_by_id(self, user_id: int, session_uuid: UUIDString) -> bool:
        return await self.__delete_session(user_id, session_uuid, soft=True)

    async def revoke_other_sessions(self, user_id: int, keep_session_uuid: UUIDString) -> None:
        for session in await self.get_user_sessions(user_id):
            if session.session_uuid == keep_session_uuid:
                continue

            await self.__delete_session(user_id, session.session_uuid, soft=True)

    async def update_session(self, updated_schema: AuthSessionInternal) -> None:
        await self.__save_session(updated_schema)

    async def session_heartbeat(self, session: AuthSessionInternal) -> None:
        session.last_used = datetime.now()
        await self.update_session(session)

    async def session_heartbeat_by_id(self, user_id: int, session_uuid: UUIDString) -> AuthSessionInternal | None:
        if (session := await self.get_session(user_id, session_uuid)) is None:
            return None

        await self.session_heartbeat(session)
        return session

    async def get_session_from_access_token(self, access_token: str) -> AuthSessionInternal:
        payload = decode_access_token_with_http_exceptions(access_token)

        if (session := await self.get_session(payload.user_id, payload.session_uuid)) is None:
            raise InvalidSessionHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        if session.access_token_uuid != payload.token_uuid:
            raise TokenExpiredHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        return session

    async def get_session_from_refresh_token(self, refresh_token: str) -> AuthSessionInternal:
        payload = decode_refresh_token_with_http_exceptions(refresh_token)

        if (session := await self.get_session(payload.user_id, payload.session_uuid)) is None:
            raise InvalidSessionHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        if session.refresh_token_uuid != payload.token_uuid:
            raise TokenExpiredHTTPException(status_code=HTTPStatus.UNAUTHORIZED)

        return session

    async def cleanup(self) -> None:  # TODO
        pass
