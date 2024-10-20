from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

import pytest

from rsqlalchemy.parse import query_to_sql
from tests.model import Base, User


@pytest.fixture(scope="module")
def get_db():
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    test_data = [
        User(name="Alice", address="123 Builder Drive"),
        User(name="Bob", address="456 Builder Avenue"),
        User(name="Charlie", address="789 Chocolate Factory Street"),
        User(name="Charlie", address="101 Flower Street"),
        User(name="Eve", address="303 River Road"),
        User(name="Frank", address="303 River Road"),
    ]
    with Session(engine) as session:
        session.add_all(test_data)
        session.commit()
    return engine


def test_eq(get_db: Engine):
    test_cases = [
        ("id==1", [1]),
        ("name==Bob", [2]),
        ("name==Charlie", [3, 4]),
        ("name==Charlie and address==*Chocolate*", [3]),
        ("name==Charlie or name==Eve or name==Frank", [3, 4, 5, 6]),
        ("name==Charlie,name==Eve,name==Frank", [3, 4, 5, 6]),
    ]
    with Session(get_db) as session:
        for query, expected in test_cases:
            result = session.scalars(
                select(User.id).where(query_to_sql(User, query))
            ).all()
            assert result == expected
