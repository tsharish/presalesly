from sqlalchemy import MetaData, schema

from app.db.base import Base
from app.db.session import with_db, engine
from app.core.constants import LANGUAGES, COUNTRIES, CURRENCIES
from app.models.shared import Language, Country, Currency


def get_shared_metadata():
    """Creates a new metadata object with only the shared tables"""
    meta = MetaData()
    for table in Base.metadata.tables.values():
        if table.schema != "tenant":
            table.tometadata(meta)
    return meta


def init_database():
    """Creates the 'shared' database schema and the shared tables"""

    with with_db(None) as db:
        """context = MigrationContext.configure(db)
        if context.get_current_revision() is not None:
            print("Database already exists.")
            return"""

        if not engine.dialect.has_schema(engine, "shared"):
            db.execute(schema.CreateSchema("shared"))

            get_shared_metadata().create_all(bind=db.connection())

            for lang in LANGUAGES:
                db.add(Language(code=lang))

            for country in COUNTRIES:
                db.add(Country(code=country))

            for currency in CURRENCIES:
                db.add(Currency(code=currency))

            db.commit()

        """ alembic_config.attributes["connection"] = db
        command.stamp(alembic_config, "head", purge=True) """
