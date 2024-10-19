from rsqlalchemy import utils


def test_split_ignore_parenth():
    test_cases = [
        ["a and (b and c or d) and e", [" and "], ["a", "(b and c or d)", "e"]],
        ["(a or b or c)", [" or "], ["(a or b or c)"]],
        ["a ( ) b", [" "], ["a", "( )", "b"]],
        ["split", ["split"], []],
        ["a and (b;(c));d", [" and ", ";"], ["a", "(b;(c))", "d"]],
        [
            "a,(b),c,(d,e),f,(g,(h,i))",
            [","],
            ["a", "(b)", "c", "(d,e)", "f", "(g,(h,i))"],
        ],
    ]
    for target, delimiter, expected in test_cases:
        actual = utils.split_query(target, delimiter)
        assert (
            expected == actual
        ), f"\nTarget: {target}\nExpected: {expected}\nActual: {actual}"


def test_split_ignore_parenth_error():
    try:
        utils.split_query("a or b or c)))))", [" or "])
    except ValueError as e:
        assert e.args == ("Invalid expression: too many right parentheses",)
    else:
        assert False, "Test should raise ValueError but didn't"
    try:
        utils.split_query("(((a or b or c", [" or "])
    except ValueError as e:
        assert e.args == ("Invalid expression: too many left parentheses",)
    else:
        assert False, "Test should raise ValueError but didn't"
