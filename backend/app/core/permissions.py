from typing import Any
from fastapi import HTTPException
from sqlalchemy import select, and_

from app.db.session import db_session
from app.core.enums import Permission
from app.models.auth import AccessControl
from app.models.user import User

permission_exception = HTTPException(
    status_code=403,
    detail="Insufficient permissions",
    headers={"WWW-Authenticate": "Bearer"},
)


def has_permission(user: User, resource: Any, permission: Permission) -> bool:
    user_principals = get_user_principals(user=user)
    resource_acl = get_resource_acl(resource=resource, permission=permission)
    for entry in resource_acl:
        if entry in user_principals:
            return True
    return False


def get_user_principals(user: User) -> set[str]:
    user_principals = set()
    user_principals.add(f"role:{user.role_id}")
    user_principals.add(f"user:{user.id}")
    return user_principals


def get_resource_acl(resource: Any, permission: Permission) -> set[str]:
    resource_acl = set()
    resource_type_id = resource.get_resource_type()
    db = db_session.get()

    results = (
        db.execute(
            select(AccessControl).where(
                and_(
                    AccessControl.resource_type_id == resource_type_id,
                    AccessControl.permission == permission.name,
                )
            )
        )
        .scalars()
        .all()
    )

    for entry in results:
        match entry.role_id:
            case "OWNER":
                resource_acl.add(f"user:{resource.owner_id}")
            case "PARENT":
                resource_acl.add(f"user:{resource.parent.owner_id}")
            case "MEMBER":
                # The members property of resource must return a list of user IDs
                formatted_members = [f"user:{member}" for member in resource.members]
                resource_acl.update(formatted_members)
            case _:
                resource_acl.add(f"role:{entry.role_id}")

    return resource_acl
