import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    user = os.getenv("POSTGRES_USER", "toby")
    password = os.getenv("POSTGRES_PASSWORD", "andy1984")
    host = os.getenv("POSTGRES_HOST", "192.168.0.150")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "pgdatabase")
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL)

def migrate():
    print(f"Connecting to {DATABASE_URL}...")
    with engine.connect() as conn:
        print("Checking for missing columns in 'mentors' table...")
        
        # Add email
        try:
            conn.execute(text("ALTER TABLE mentors ADD COLUMN email VARCHAR(255) UNIQUE"))
            conn.commit()
            print("Successfully added 'email' column.")
        except Exception as e:
            print(f"Note: 'email' column might already exist or error: {e}")

        # Add status
        try:
            conn.execute(text("ALTER TABLE mentors ADD COLUMN status VARCHAR(20) DEFAULT 'active'"))
            conn.commit()
            print("Successfully added 'status' column.")
        except Exception as e:
            print(f"Note: 'status' column might already exist or error: {e}")

        # Add verification_token
        try:
            conn.execute(text("ALTER TABLE mentors ADD COLUMN verification_token VARCHAR(100)"))
            conn.commit()
            print("Successfully added 'verification_token' column.")
        except Exception as e:
            print(f"Note: 'verification_token' column might already exist or error: {e}")

    print("Migration finished.")

if __name__ == "__main__":
    migrate()
