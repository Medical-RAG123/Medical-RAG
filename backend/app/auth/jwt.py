from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.auth.config.settings import settings


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token."""

    payload = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    """Validate and decode a JWT access token."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        return payload

    except JWTError as exc:
        raise ValueError("Invalid or expired access token") from exc
