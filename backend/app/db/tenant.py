import sqlalchemy as sa
from sqlalchemy import select

from app.db.base import Base
from app.db.session import with_db

"""Import all the SQLAlchemy models"""
from app.models.shared import Tenant, Language, Country, Currency
from app.models.auth import Role, ResourceType, AccessControl
from app.models.user import User
from app.models.opp_stage import *
from app.models.industry import *
from app.models.account import *
from app.models.opp_template import *
from app.models.opportunity import *
from app.models.task import *
from app.models.answer import *

from app.db.init_tenant import (
    init_roles,
    init_resource_types,
    init_access_control,
    init_user,
)


def create_tenant(name: str, schema: str, host: str) -> None:
    """
    Creates a tenant schema and the tenant specific tables, and initializes the tenant
    """
    with with_db(schema) as db:
        """context = MigrationContext.configure(db.connection())
        script = alembic.script.ScriptDirectory.from_config(alembic_config)
        if context.get_current_revision() != script.get_current_head():
            raise RuntimeError(
                "Database is not up-to-date. Execute migrations before adding new tenants."
            )"""

        tenant = Tenant(
            name=name,
            schema=schema,
            host=host,
        )
        db.add(tenant)

        db.execute(sa.schema.CreateSchema(schema))
        Base.metadata.create_all(bind=db.connection())
        init_roles(db)
        init_resource_types(db)
        init_access_control(db)
        init_user(db)

        db.commit()


def get_tenants() -> list[Tenant] | None:
    """Returns all the tenants"""
    with with_db(None) as db:
        tenants = db.execute(select(Tenant)).scalars().all()
    return tenants


def delete_tenant(name: str) -> None:
    """Drops the tenant schema and removes the tenant from the tenant table"""
    with with_db(None) as db:
        tenant = db.execute(select(Tenant).where(Tenant.name == name)).scalar_one_or_none()

    if not tenant:
        raise Exception("No tenant matches the name")

    with with_db(None) as db:
        db.delete(tenant)
        db.execute(sa.schema.DropSchema(tenant.schema, cascade=True))
        db.commit()
