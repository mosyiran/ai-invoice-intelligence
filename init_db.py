
from app.db.database import engine
from app.db.base import Base

# Import models so SQLAlchemy registers them
from app.models.invoice import Invoice


def init_database():

    Base.metadata.create_all(bind=engine)

    print("Database created successfully!")
    print("Invoice table created successfully!")


if __name__ == "__main__":
    init_database()
