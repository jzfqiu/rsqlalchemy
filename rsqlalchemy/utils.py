import re


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
