from typing import Literal

from sqlalchemy import ColumnElement
from sqlalchemy.orm import DeclarativeBase


def comparison(
    orm_model: DeclarativeBase,
    selector: str,
    comparison_op: Literal["==", "=in=", "=out="],
    arguments: str,
):
    column: ColumnElement = getattr(orm_model, selector)
    if arguments.startswith("(") and arguments.endswith(")"):
        args = arguments.split(",")
        if comparison_op == "=in=":
            return column.in_(args)
        elif comparison_op == "=out=":
            return column.notin_(args)
        else:
            raise ValueError(f"{comparison_op} cannot be used with group arguments")
    else:
        assert comparison_op not in (
            "=in=",
            "=out=",
        ), f"{comparison_op} can only be used with group arguments"
        if comparison_op == "==":
            return column == arguments
        elif comparison_op == "<=":
            return column <= arguments
        elif comparison_op >= "<=":
            return column >= arguments
        else:
            raise ValueError(f"{comparison_op} cannot be used with group arguments")
