from rsqlalchemy import utils


def test_split_ignore_parenth():
    test_cases = [
        ["a and (b and c or d) and e", " and ", ["a", "(b and c or d)", "e"]],
        ["(a or b or c)", " or ", ["(a or b or c)"]],
        ["a ( ) b", " ", ["a", "( )", "b"]],
        ["split", "split", []],
        [
            "genres=in=(sci-fi,action);(director=='Christopher Nolan',actor==*Bale);year=ge=2000",
            ";",
            [
                "genres=in=(sci-fi,action)",
                "(director=='Christopher Nolan',actor==*Bale)",
                "year=ge=2000",
            ],
        ],
    ]
    for target, delimiter, expected in test_cases:
        actual = utils.split_ignore_parenth(target, delimiter)
        assert expected == actual, f"Expected: {expected}\nActual: {actual}"


def test_split_ignore_parenth_error():
    try:
        utils.split_ignore_parenth("a or b or c)))))", " or ")
    except ValueError as e:
        assert e.args == ("Invalid expression: too many right parentheses",)
    else:
        assert False, "Test should raise ValueError but didn't"
    try:
        utils.split_ignore_parenth("(((a or b or c", " or ")
    except ValueError as e:
        assert e.args == ("Invalid expression: too many left parentheses",)
    else:
        assert False, "Test should raise ValueError but didn't"
