def split_ignore_parenth(target: str, delimiter: str) -> list[str]:
    res = []
    l, r = 0, 0
    n_parenth = 0
    while r < len(target):
        if target[r] == "(":
            n_parenth += 1
        if target[r] == ")":
            n_parenth -= 1
        if n_parenth < 0:
            raise ValueError("Invalid expression: too many right parentheses")
        if n_parenth == 0 and target[r : r + len(delimiter)] == delimiter:
            if l != r:
                res.append(target[l:r])
            l, r = r + len(delimiter), r + len(delimiter)
        else:
            r += 1
    if n_parenth > 0:
        raise ValueError("Invalid expression: too many left parentheses")
    if l != r:
        res.append(target[l:r])
    return res
