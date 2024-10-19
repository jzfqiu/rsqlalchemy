def split_ignore_parenth(target: str, delimiter: str) -> list[str]:
    res = []
    left, right = 0, 0
    n_parenth = 0
    while right < len(target):
        if target[right] == "(":
            n_parenth += 1
        if target[right] == ")":
            n_parenth -= 1
        if n_parenth < 0:
            raise ValueError("Invalid expression: too many right parentheses")
        if n_parenth == 0 and target[right : right + len(delimiter)] == delimiter:
            if left != right:
                res.append(target[left:right])
            left, right = right + len(delimiter), right + len(delimiter)
        else:
            right += 1
    if n_parenth > 0:
        raise ValueError("Invalid expression: too many left parentheses")
    if left != right:
        res.append(target[left:right])
    return res
