from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./reviews.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    """
    Create the database tables based on the defined models.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Create a new database session.
    """
    with Session(engine) as session:
        yield session

