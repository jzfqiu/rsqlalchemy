from sqlalchemy import ColumnElement, and_, or_

from rsqlalchemy.parse import comparison, expression_and, expression_or
from tests.model import User


def _compile(expression: ColumnElement) -> str:
    return str(expression.compile(compile_kwargs={"literal_binds": True}))


def test_comparison():
    test_cases = [
        ("id==1", User.id == "1"),
        ("id>=1", User.id >= "1"),
        ("id<=10", User.id <= "10"),
        ("name=in=(a,b,c)", User.name.in_(["a", "b", "c"])),
        ("address==null", User.address.is_(None)),
        ("name==*abc", User.name.like("%abc")),
        ("name==*abc*", User.name.like("%abc%")),
        ("name==ab*c", User.name.like("ab%c")),
        (
            "address=out=(a,b,c)",
            User.address.notin_(["a", "b", "c"]),
        ),
        (
            "address=in=(null,a,b)",
            User.address.in_([None, "a", "b"]),
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


def test_expression_or():
    test_cases = [
        ("id==1,id==2", or_(User.id == "1", User.id == "2")),
        ("id==1 or id==2", or_(User.id == "1", User.id == "2")),
        ("id==1 or id==2,id==3", or_(User.id == "1", User.id == "2", User.id == "3")),
        (
            "id==1 or id==2 and id==3",
            or_(
                User.id == "1",
                and_(User.id == "2", User.id == "3"),
            ),
        ),
        (
            "(id==1 or id==2) and id==3",
            and_(
                or_(User.id == "1", User.id == "2"),
                User.id == "3",
            ),
        ),
        (
            "(id==1 or id==2) and id==3",
            and_(
                or_(User.id == "1", User.id == "2"),
                User.id == "3",
            ),
        ),
        (
            "(id==1 or id==2 and id==3) and id==4",
            and_(
                or_(User.id == "1", and_(User.id == "2", User.id == "3")),
                User.id == "4",
            ),
        ),
        (
            "((id==1 or id==2) and id==3) and id==4",
            and_(
                and_(or_(User.id == "1", User.id == "2"), User.id == "3"),
                User.id == "4",
            ),
        ),
    ]
    for query, expected in test_cases:
        assert _compile(expression_or(User, query)) == _compile(expected)
