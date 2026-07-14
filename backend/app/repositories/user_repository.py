from sqlalchemy.orm import Session

# OLD
from app.models.user import User

# NEW
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserRegister


def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user: UserRegister,
    hashed_password: str,
):
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
def save_refresh_token(
    db: Session,
    token: str,
    user_id: int,
    expires_at,
) -> RefreshToken:

    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token(
    db: Session,
    token: str,
) -> RefreshToken | None:

    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token,
        )
        .first()
    )


def delete_refresh_token(
    db: Session,
    db_token: RefreshToken,
) -> None:

    db.delete(db_token)
    db.commit()

def update_user_password(
    db: Session,
    user: User,
    hashed_password: str,
) -> User:
    user.password = hashed_password

    db.commit()
    db.refresh(user)

    return user

def verify_user_email(
    db: Session,
    user: User,
) -> User:
    user.is_verified = True

    db.commit()
    db.refresh(user)

    return user