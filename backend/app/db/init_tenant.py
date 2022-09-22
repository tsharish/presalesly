from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.auth import AccessControl, ResourceType, Role
from app.models.user import User
from app.core.security import get_hashed_password


def init_roles(db: Session) -> None:
    """Initializes user roles"""
    roles = [
        {"id": "ADMIN", "is_reserved": False, "is_standard": True},
        {"id": "SUPER", "is_reserved": False, "is_standard": True},
        {"id": "PROF", "is_reserved": False, "is_standard": True},
        {"id": "STANDARD", "is_reserved": False, "is_standard": True},
        {"id": "OWNER", "is_reserved": True, "is_standard": True},
        {"id": "PARENT", "is_reserved": True, "is_standard": True},
        {"id": "TECHNICAL", "is_reserved": True, "is_standard": True},
    ]
    for role in roles:
        db.add(Role(**role))
    # Flush seems to be needed here to ensure sequence of inserts, otherwise it errors out
    db.flush()


def init_resource_types(db: Session) -> None:
    """Initializes resource types such as account"""
    resource_types = [
        {"id": "setting"},
        {"id": "account"},
        {"id": "opportunity"},
        {"id": "task"},
        {"id": "answer"},
    ]
    for resource_type in resource_types:
        db.add(ResourceType(**resource_type))
    db.flush()


def init_access_control(db: Session) -> None:
    """Initializes the Access Control entries"""
    access_control_entries = [
        {"resource_type_id": "setting", "role_id": "ADMIN", "permission": "create"},
        {"resource_type_id": "setting", "role_id": "ADMIN", "permission": "read"},
        {"resource_type_id": "setting", "role_id": "ADMIN", "permission": "update"},
        {"resource_type_id": "setting", "role_id": "ADMIN", "permission": "delete"},
        {"resource_type_id": "setting", "role_id": "SUPER", "permission": "read"},
        {"resource_type_id": "setting", "role_id": "PROF", "permission": "read"},
        {"resource_type_id": "setting", "role_id": "STANDARD", "permission": "read"},
        {"resource_type_id": "account", "role_id": "ADMIN", "permission": "create"},
        {"resource_type_id": "account", "role_id": "ADMIN", "permission": "read"},
        {"resource_type_id": "account", "role_id": "ADMIN", "permission": "update"},
        {"resource_type_id": "account", "role_id": "ADMIN", "permission": "delete"},
        {"resource_type_id": "account", "role_id": "SUPER", "permission": "create"},
        {"resource_type_id": "account", "role_id": "SUPER", "permission": "read"},
        {"resource_type_id": "account", "role_id": "SUPER", "permission": "update"},
        {"resource_type_id": "account", "role_id": "SUPER", "permission": "delete"},
        {"resource_type_id": "opportunity", "role_id": "ADMIN", "permission": "create"},
        {"resource_type_id": "opportunity", "role_id": "ADMIN", "permission": "read"},
        {"resource_type_id": "opportunity", "role_id": "ADMIN", "permission": "update"},
        {"resource_type_id": "opportunity", "role_id": "ADMIN", "permission": "delete"},
        {"resource_type_id": "opportunity", "role_id": "SUPER", "permission": "create"},
        {"resource_type_id": "opportunity", "role_id": "SUPER", "permission": "read"},
        {"resource_type_id": "opportunity", "role_id": "SUPER", "permission": "update"},
        {"resource_type_id": "opportunity", "role_id": "SUPER", "permission": "delete"},
        {"resource_type_id": "opportunity", "role_id": "PROF", "permission": "create"},
        {"resource_type_id": "opportunity", "role_id": "PROF", "permission": "read"},
        {"resource_type_id": "opportunity", "role_id": "PROF", "permission": "update"},
        {"resource_type_id": "opportunity", "role_id": "PROF", "permission": "delete"},
        {"resource_type_id": "opportunity", "role_id": "OWNER", "permission": "read"},
        {"resource_type_id": "opportunity", "role_id": "OWNER", "permission": "update"},
        {"resource_type_id": "opportunity", "role_id": "OWNER", "permission": "delete"},
        {
            "resource_type_id": "opportunity",
            "role_id": "STANDARD",
            "permission": "create",
        },
        {"resource_type_id": "task", "role_id": "ADMIN", "permission": "create"},
        {"resource_type_id": "task", "role_id": "ADMIN", "permission": "read"},
        {"resource_type_id": "task", "role_id": "ADMIN", "permission": "update"},
        {"resource_type_id": "task", "role_id": "ADMIN", "permission": "delete"},
        {"resource_type_id": "task", "role_id": "SUPER", "permission": "create"},
        {"resource_type_id": "task", "role_id": "SUPER", "permission": "read"},
        {"resource_type_id": "task", "role_id": "SUPER", "permission": "update"},
        {"resource_type_id": "task", "role_id": "SUPER", "permission": "delete"},
        {"resource_type_id": "task", "role_id": "PROF", "permission": "create"},
        {"resource_type_id": "task", "role_id": "PROF", "permission": "read"},
        {"resource_type_id": "task", "role_id": "PROF", "permission": "update"},
        {"resource_type_id": "task", "role_id": "PROF", "permission": "delete"},
        {"resource_type_id": "task", "role_id": "OWNER", "permission": "read"},
        {"resource_type_id": "task", "role_id": "OWNER", "permission": "update"},
        {"resource_type_id": "task", "role_id": "OWNER", "permission": "delete"},
        {"resource_type_id": "task", "role_id": "PARENT", "permission": "create"},
        {"resource_type_id": "task", "role_id": "PARENT", "permission": "read"},
        {"resource_type_id": "task", "role_id": "PARENT", "permission": "update"},
        {"resource_type_id": "task", "role_id": "PARENT", "permission": "delete"},
        {"resource_type_id": "answer", "role_id": "ADMIN", "permission": "create"},
        {"resource_type_id": "answer", "role_id": "ADMIN", "permission": "read"},
        {"resource_type_id": "answer", "role_id": "ADMIN", "permission": "update"},
        {"resource_type_id": "answer", "role_id": "ADMIN", "permission": "delete"},
        {"resource_type_id": "answer", "role_id": "SUPER", "permission": "create"},
        {"resource_type_id": "answer", "role_id": "SUPER", "permission": "read"},
        {"resource_type_id": "answer", "role_id": "SUPER", "permission": "update"},
        {"resource_type_id": "answer", "role_id": "SUPER", "permission": "delete"},
        {"resource_type_id": "answer", "role_id": "PROF", "permission": "create"},
        {"resource_type_id": "answer", "role_id": "PROF", "permission": "read"},
        {"resource_type_id": "answer", "role_id": "PROF", "permission": "update"},
        {"resource_type_id": "answer", "role_id": "PROF", "permission": "delete"},
    ]
    for entry in access_control_entries:
        db.add(AccessControl(**entry))
    db.flush()


def init_user(db: Session) -> None:
    """Initializes the Initial user"""
    initial_user = User(
        email=settings.INITIAL_EMAIL,
        password=get_hashed_password(settings.INITIAL_PASSWORD),
        role_id=settings.INITIAL_USER_ROLE,
    )
    db.add(initial_user)
    db.flush()
