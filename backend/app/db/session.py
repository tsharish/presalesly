from contextlib import contextmanager
from contextvars import ContextVar
from fastapi import Depends, HTTPException, Request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.shared import Tenant

tenants_cache = dict[str, Tenant]()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
db_session: ContextVar[Session] = ContextVar("db_session")
db_schema: ContextVar[str] = ContextVar("db_schema")


@contextmanager
def with_db(tenant_schema: str | None):
    """Returns a DB session with a specific tenant schema"""
    if tenant_schema:
        schema_translate_map = dict(tenant=tenant_schema)
    else:
        schema_translate_map = None

    connectable = engine.execution_options(schema_translate_map=schema_translate_map)

    try:
        db = Session(autocommit=False, autoflush=False, bind=connectable)
        yield db
    finally:
        db.close()


def get_tenant(req: Request) -> Tenant:
    """Returns the tenant based on the host in the request"""
    host_without_port = req.headers["host"].split(":", 1)[0]

    if host_without_port in tenants_cache:
        return tenants_cache[host_without_port]

    with with_db(None) as db:
        tenant = db.execute(
            select(Tenant).where(Tenant.host == host_without_port)
        ).scalar_one_or_none()

    if tenant is None:
        raise HTTPException(status_code=403, detail="No tenant was found")

    tenants_cache[host_without_port] = tenant
    return tenant


def get_db(tenant: Tenant = Depends(get_tenant)):
    """Dependency to get the DB session"""
    with with_db(tenant.schema) as db:  # type: ignore
        yield db


def get_schema_from_request(tenant: Tenant = Depends(get_tenant)):
    """Returns the DB schema based on the host in the request"""
    return tenant.schema
