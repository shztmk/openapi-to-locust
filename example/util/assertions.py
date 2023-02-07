import re


def assert_str_matches(pattern: str):
    class AssertStrMatches(str):
        __slots__ = []

        def __init__(self, string: str):
            assert re.fullmatch(pattern, string) is not None

    return AssertStrMatches


def assert_str_min_length(min_length: int):
    class AssertStrMinLength(str):
        __slots__ = []

        def __init__(self, string: str):
            assert len(string) >= min_length

    return AssertStrMinLength


def assert_str_max_length(max_length: int):
    class AssertStrMaxLength(str):
        __slots__ = []

        def __init__(self, string: str):
            assert len(string) <= max_length

    return AssertStrMaxLength


def assert_int_minimum(minimum: int, exclusive_minimum: bool = False):
    class AssertIntMinimum(int):
        __slots__ = []

        def __init__(self, integer: int):
            assert integer > minimum or (not exclusive_minimum and integer == minimum)

    return AssertIntMinimum


def assert_int_maximum(maximum: int, exclusive_maximum: bool = False):
    class AssertIntMaximum(int):
        __slots__ = []

        def __init__(self, integer: int):
            assert integer < maximum or (not exclusive_maximum and integer == maximum)

    return AssertIntMaximum
