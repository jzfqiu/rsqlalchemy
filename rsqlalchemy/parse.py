import re
from sqlalchemy import ColumnElement, and_, or_
from sqlalchemy.orm import DeclarativeBase


def is_group(s: str) -> bool:
    return s.startswith("(") and s.endswith(")")


def split_query(target: str, delimiters: list[str]) -> list[str]:
    level = 0
    preserved: list[str] = []
    left = 0
    marker = "\uffff"
    marked = ""

    # find all substring enclosed in parenthesis
    for right in range(len(target)):
        if target[right] == "(":
            if level == 0:
                left = right
                marked += marker
            level += 1
        elif target[right] == ")":
            level -= 1
            if level == 0:
                preserved.append(target[left : right + 1])
        if level < 0:
            raise ValueError("Invalid expression: too many right parentheses")
        elif level == 0 and target[right] != ")":
            marked += target[right]
    if level > 0:
        raise ValueError("Invalid expression: too many left parentheses")

    # split and put content inside parentheses back in place
    result = []
    regex_pattern = "|".join(map(re.escape, delimiters))
    for word in re.split(regex_pattern, marked):
        if word == "":
            continue
        elif marker in word:
            result.append(word.replace(marker, preserved.pop(0)))
        else:
            result.append(word)

    return result


def query_to_sql(orm_model: DeclarativeBase, s: str) -> ColumnElement:
    return expression_or(orm_model, s)


def expression_or(orm_model: DeclarativeBase, s: str) -> ColumnElement:
    children = split_query(s, [" or ", ","])
    parsed_children = []
    if len(children) <= 1:
        return expression_and(orm_model, s)
    for child in children:
        if is_group(child):
            parsed_children.append(expression_or(orm_model, child[1:-1]))
        else:
            parsed_children.append(expression_and(orm_model, child))
    return or_(*parsed_children)


def expression_and(orm_model: DeclarativeBase, s: str) -> ColumnElement:
    children = split_query(s, [" and ", ";"])
    parsed_children = []
    if len(children) <= 1:
        return comparison(orm_model, s)
    for child in children:
        if is_group(child):
            parsed_children.append(expression_or(orm_model, child[1:-1]))
        else:
            parsed_children.append(comparison(orm_model, child))
    return and_(*parsed_children)


def comparison(orm_model: DeclarativeBase, s: str) -> ColumnElement:
    for comparison_op in ["==", "=in=", "=out=", "<=", ">="]:
        if comparison_op in s:
            selector, arguments = s.split(comparison_op)
            break
    else:
        raise ValueError(f"{s} is not a supported comparison")

    column: ColumnElement = getattr(orm_model, selector)

    if is_group(arguments):
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
        if arguments and "*" in arguments:
            return column.like(arguments.replace("*", "%"))
        else:
            return column == arguments
    elif comparison_op == "<=":
        return column <= arguments
    elif comparison_op == ">=":
        return column >= arguments
    else:
        raise ValueError(f"{comparison_op} cannot be used with group arguments")
