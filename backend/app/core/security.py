from datetime import datetime, timedelta, timezone

from jose import JWSError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# Hash a plain password before storing it in the database.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password against the stored hash.
def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# Common function used to generate JWT tokens.
def _create_token(
    data: dict,
    expires_delta: timedelta,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc,
    ) + expires_delta

    to_encode.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# Create a short-lived access token.
def create_access_token(
    data: dict,
) -> str:
    payload = data.copy()

    payload["type"] = "access"

    return _create_token(
        data=payload,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


# Create a long-lived refresh token.
def create_refresh_token(
    data: dict,
) -> str:
    payload = data.copy()

    payload["type"] = "refresh"

    return _create_token(
        data=payload,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )

# NEW
# Create a short-lived password reset token.
def create_reset_token(
    data: dict,
) -> str:
    payload = data.copy()

    payload["type"] = "reset"

    return _create_token(
        data=payload,
        expires_delta=timedelta(
            minutes=15,
        ),
    )
# NEW
# Create an email verification token.
def create_verification_token(
    data: dict,
) -> str:
    payload = data.copy()

    payload["type"] = "verify"

    return _create_token(
        data=payload,
        expires_delta=timedelta(
            hours=24,
        ),
    )

def verify_refresh_token(
    token: str,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise ValueError

        return payload

    except (JWTError, ValueError):
        raise ValueError(
            "Invalid refresh token."
        )

# NEW
# Verify password reset token.
def verify_reset_token(
    token: str,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "reset":
            raise ValueError

        return payload

    except (JWTError, ValueError):
        raise ValueError(
            "Invalid reset token.",
        )

# NEW
# Verify email verification token.
def verify_verification_token(
    token: str,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "verify":
            raise ValueError

        return payload

    except (JWTError, ValueError):
        raise ValueError(
            "Invalid verification token.",
        )