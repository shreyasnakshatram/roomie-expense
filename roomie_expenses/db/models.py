import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float


base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "roomie_expenses.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    source_of_expense = Column(String, unique=False)
    amount = Column(Float, unique=False)
    added_by_id = Column(Integer, ForeignKey("users.id"))
    month = Column(Integer, unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
