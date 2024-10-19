from sqlalchemy import ColumnElement
from sqlalchemy.orm import DeclarativeBase


def comparison(orm_model: DeclarativeBase, s: str):
    for comparison_op in ["==", "=in=", "=out=", "<=", ">="]:
        if comparison_op in s:
            selector, arguments = s.split(comparison_op)
            break
    else:
        raise ValueError(f"{s} is not a supported comparison")

    column: ColumnElement = getattr(orm_model, selector)

    if arguments.startswith("(") and arguments.endswith(")"):
        args = arguments.strip("()").split(",")
        args = [None if x == "null" else x for x in args]
        if comparison_op == "=in=":
            return column.in_(args)
        elif comparison_op == "=out=":
            return column.notin_(args)
        else:
            raise ValueError(f"{comparison_op} cannot be used with group arguments")

    if arguments == "null":
        assert comparison_op == "==", "null cannot be used with other operators"
        arguments = None

    if comparison_op == "==":
        return column == arguments
    elif comparison_op == "<=":
        return column <= arguments
    elif comparison_op >= "<=":
        return column >= arguments
    else:
        raise ValueError(f"{comparison_op} cannot be used with group arguments")
