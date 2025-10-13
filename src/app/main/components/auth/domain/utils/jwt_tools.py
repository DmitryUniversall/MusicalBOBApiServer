import uuid
from typing import Dict, Any, Union, TYPE_CHECKING

import jwt

from src.base.state import project_settings
from src.base.utils.types import UUIDString, JsonDict

if TYPE_CHECKING:
    from src.app.main.components.auth.domain import AccessTokenPayload, RefreshTokenPayload


def generate_jwt_token_id() -> str:
    return str(uuid.uuid4())


def create_jwt_token(*, payload: JsonDict, exp: Union[int, float]) -> str:
    encoded_jwt = jwt.encode(
        payload={
            "exp": exp,
            **payload
        },
        key=project_settings.SECRET_KEY,
        algorithm=project_settings.TOKEN_ENCRYPTION_ALGORITHM
    )

    return encoded_jwt


def decode_jwt_token(token: str) -> Dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=project_settings.SECRET_KEY,
        algorithms=[project_settings.TOKEN_ENCRYPTION_ALGORITHM]
    )


def create_access_token_with_payload(payload: 'AccessTokenPayload') -> str:
    return create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())


def create_refresh_token_with_payload(payload: 'RefreshTokenPayload') -> str:
    return create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())


def create_access_token(user_id: int, session_uuid: UUIDString, token_uuid: str | None = None) -> str:
    from src.app.main.components.auth.domain import AccessTokenPayload

    payload: AccessTokenPayload
    if token_uuid is not None:
        payload = AccessTokenPayload(user_id=user_id, session_uuid=session_uuid, token_uuid=token_uuid)
    else:
        payload = AccessTokenPayload(user_id=user_id, session_uuid=session_uuid)

    return create_access_token_with_payload(payload=payload)


def create_refresh_token(user_id: int, session_uuid: UUIDString, token_uuid: str | None = None) -> str:
    from src.app.main.components.auth.domain import RefreshTokenPayload

    payload: RefreshTokenPayload
    if token_uuid is not None:
        payload = RefreshTokenPayload(user_id=user_id, session_uuid=session_uuid, token_uuid=token_uuid)
    else:
        payload = RefreshTokenPayload(user_id=user_id, session_uuid=session_uuid)

    return create_refresh_token_with_payload(payload=payload)
