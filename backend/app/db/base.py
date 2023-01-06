from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, declared_attr


class CustomBase:
    """Base class which provides automated table name and
    resource type (for permissions)"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # type: ignore

    @classmethod
    def get_resource_type(cls):
        return cls.__tablename__


metadata = MetaData(schema="tenant")
Base = declarative_base(cls=CustomBase, metadata=metadata)


def get_class_by_tablename(tablename: str):
    """Return class reference mapped to table

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for cls in Base.registry._class_registry.values():  # type: ignore
        if hasattr(cls, "__table__") and cls.__table__.name == tablename:
            # Replaced 'fullname' with 'name' above since fullname included the schema name ('tenant') also
            return cls
