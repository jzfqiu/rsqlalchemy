from typing import Optional
from sqlalchemy import ColumnElement, String, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rsqlalchemy.parse import comparison, expression_and, expression_or


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
        ("id==1", User.id == "1"),
        ("id>=1", User.id >= "1"),
        ("id<=10", User.id <= "10"),
        ("name=in=(a,b,c)", User.name.in_(["a", "b", "c"])),
        ("fullname==null", User.fullname.is_(None)),
        (
            "fullname=out=(a,b,c)",
            User.fullname.notin_(["a", "b", "c"]),
        ),
        (
            "fullname=in=(null,a,b)",
            User.fullname.in_([None, "a", "b"]),
        ),
    ]
    for query, expected in test_cases:
        assert _compile(comparison(User, query)) == _compile(expected)


def test_expression_and():
    test_cases = [
        ("id==1;id==2", and_(User.id == "1", User.id == "2")),
        ("id==1 and id==2", and_(User.id == "1", User.id == "2")),
        ("id==1 and id==2;id==3", and_(User.id == "1", User.id == "2", User.id == "3")),
        (
            "id==1 and (id==2;id==3)",
            and_(User.id == "1", and_(User.id == "2", User.id == "3")),
        ),
        (
            "(id>=1 and name=in=(a,b,c)) and (id==2;id==3)",
            and_(
                and_(User.id >= "1", User.name.in_(["a", "b", "c"])),
                and_(User.id == "2", User.id == "3"),
            ),
        ),
    ]
    for query, expected in test_cases:
        assert _compile(expression_and(User, query)) == _compile(expected)
