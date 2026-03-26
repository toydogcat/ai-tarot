import sys
import os
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import (
    FACTORY_DATABASE_URL, PROJECT_DATABASE_URL, 
    factory_metadata, project_metadata,
    mentors, mentor_friends, mentor_messages
)
from core.logger import get_logger

logger = get_logger("upgrade")

def create_database_if_not_exists():
    """Connect to 'postgres' default DB to create the 'ai-factory' DB"""
    # Extract base connection info (without DB name)
    base_url = FACTORY_DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
    
    db_name = FACTORY_DATABASE_URL.rsplit('/', 1)[1]
    
    with engine.connect() as conn:
        exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")).first()
        if not exists:
            logger.info(f"Creating database: {db_name}")
            conn.execute(text(f"CREATE DATABASE \"{db_name}\""))
        else:
            logger.info(f"Database {db_name} already exists.")

def migrate_data():
    """Migrate mentors, friends, and messages from Project DB to Factory DB"""
    p_engine = create_engine(PROJECT_DATABASE_URL)
    f_engine = create_engine(FACTORY_DATABASE_URL)
    
    # Initialize tables in new DB
    factory_metadata.create_all(f_engine)
    logger.info("Initialized tables in Factory DB.")

    tables_to_migrate = [
        ('mentors', mentors),
        ('mentor_friends', mentor_friends),
        ('mentor_messages', mentor_messages)
    ]

    with p_engine.connect() as p_conn:
        with f_engine.connect() as f_conn:
            for table_name, table_obj in tables_to_migrate:
                # 1. Check if there's data to migrate
                try:
                    data = p_conn.execute(select(table_obj)).all()
                    if not data:
                        logger.info(f"No data found in {table_name} (Project DB). Skipping.")
                        continue
                    
                    logger.info(f"Migrating {len(data)} records for {table_name}...")
                    
                    # 2. Insert into Factory DB (ignoring duplicates)
                    for row in data:
                        try:
                            # Convert Row to dict
                            row_dict = dict(row._mapping)
                            f_conn.execute(table_obj.insert().values(**row_dict))
                            f_conn.commit()
                        except Exception as e:
                            # Likely already exists
                            f_conn.rollback()
                            pass
                    
                    f_conn.commit()
                    logger.info(f"Successfully migrated {table_name}.")
                except Exception as e:
                    logger.warning(f"Failed to read/migrate {table_name}: {e}")

if __name__ == "__main__":
    try:
        create_database_if_not_exists()
        migrate_data()
        logger.info("Database upgrade and migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
