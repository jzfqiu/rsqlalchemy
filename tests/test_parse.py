from typing import Optional
from sqlalchemy import ColumnElement, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rsqlalchemy.parse import comparison


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    fullname: Mapped[Optional[str]]


def _compile(expression: ColumnElement) -> str:
    return str(expression.compile(compile_kwargs={"literal_binds": True}))


def test_comparison():
    test_cases = [
        (comparison(User, "id==1"), User.id == "1"),
        (comparison(User, "name=in=(a,b,c)"), User.name.in_(["a", "b", "c"])),
        (
            comparison(User, "fullname=out=(a,b,c)"),
            User.fullname.notin_(["a", "b", "c"]),
        ),
        (comparison(User, "fullname==null"), User.fullname.is_(None)),
        (
            comparison(User, "fullname=in=(null,a,b)"),
            User.fullname.in_([None, "a", "b"]),
        ),
    ]
    for actual, expected in test_cases:
        assert _compile(actual) == _compile(expected)
